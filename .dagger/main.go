// Dagger module for testing RPM spec files
//
// This module provides functions to test and validate RPM spec files
// used in Fedora COPR builds.

package main

import (
	"context"
	"dagger/copr/internal/dagger"
	"fmt"
	"path"
	"strings"
	"sync"
)

// validFedoraVersions is an allowlist of supported Fedora versions.
var validFedoraVersions = map[string]bool{
	"40": true,
	"41": true,
	"42": true,
	"43": true,
	"44": true,
}

// invalidPathChars are shell metacharacters that must not appear in spec paths.
const invalidPathChars = ";|&`$(){} \t"

type Copr struct{}

// shC returns cmd wrapped in `sh -c` for shell pipeline execution.
func shC(cmd string) []string {
	return []string{"sh", "-c", cmd}
}

// validateInputs checks fedoraVersion and specFile for known-bad values
// before they are interpolated into container commands.
func validateInputs(fedoraVersion, specFile string) error {
	if !validFedoraVersions[fedoraVersion] {
		return fmt.Errorf("unsupported Fedora version %q: must be one of 40, 41, 42, 43, 44", fedoraVersion)
	}
	if strings.ContainsAny(specFile, invalidPathChars) {
		return fmt.Errorf("specFile path %q contains invalid characters", specFile)
	}
	if !strings.HasSuffix(specFile, ".spec") {
		return fmt.Errorf("specFile %q does not have a .spec extension", specFile)
	}
	return nil
}

// baseContainer returns a Fedora container with the RPM build toolchain
// pre-installed. This layer is shared and cached across all spec builds.
func (m *Copr) baseContainer(fedoraVersion string) *dagger.Container {
	return dag.Container().
		From(fmt.Sprintf("quay.io/fedora/fedora:%s", fedoraVersion)).
		WithExec([]string{
			"dnf", "install", "-y",
			"ca-certificates", "curl", "wget", "file",
			"dnf-plugins-core", "rpm", "rpm-build", "rpmdevtools",
		})
}

// BuildSpecFile builds a single RPM spec file inside a Fedora container.
//
// extraCoprRepos is an optional list of COPR repositories to enable before
// installing build dependencies (e.g. "myriad-sun/ghostty").
func (m *Copr) BuildSpecFile(
	ctx context.Context,
	// repository root
	// +defaultPath="/"
	source *dagger.Directory,
	// spec file to be built (e.g. "zed/zed.spec")
	specFile string,
	// fedora version to build against
	// +default="43"
	fedoraVersion string,
	// additional COPR repositories to enable (optional)
	// +optional
	extraCoprRepos []string,
) (string, error) {
	if err := validateInputs(fedoraVersion, specFile); err != nil {
		return "", err
	}

	specFileName := path.Base(specFile)
	specFileDir := path.Dir(specFile)
	specDest := fmt.Sprintf("/root/rpmbuild/SPECS/%s", specFileName)

	// Start from the shared cached base image.
	container := m.baseContainer(fedoraVersion).
		WithMountedDirectory("/workspace", source).
		WithWorkdir("/workspace")

	// Enable only the COPR repos required by this specific spec.
	for _, repo := range extraCoprRepos {
		container = container.WithExec(shC(fmt.Sprintf("dnf copr enable -y %s", repo)))
	}

	return container.
		WithExec([]string{"rpmdev-setuptree"}).

		// Copy spec file into the RPM build tree.
		WithExec([]string{"cp", specFile, specDest}).

		// Copy well-known source file types from the spec directory to SOURCES.
		WithExec(shC(fmt.Sprintf(
			"find %s -type f \\( -name '*.desktop' -o -name '*.json' -o -name '*.sh' -o -name '*.conf' -o -name '*.patch' \\) -exec cp {} /root/rpmbuild/SOURCES/ \\;",
			specFileDir,
		))).

		// Copy extensionless text/script files (e.g. zen-browser launcher).
		WithExec(shC(fmt.Sprintf(
			"find %s -type f ! -name '*.spec' ! -name '*.md' ! -name '.*' -exec sh -c 'file \"$1\" | grep -q \"text\\|script\" && cp \"$1\" /root/rpmbuild/SOURCES/' _ {} \\;",
			specFileDir,
		))).

		// Validate spec file syntax before doing any network work.
		WithExec([]string{"rpmspec", "-q", "--srpm", specDest}).

		// Download source archives declared in the spec.
		WithExec([]string{"spectool", "-g", "-R", specDest}).

		// Install build dependencies declared in the spec.
		WithExec([]string{"dnf", "builddep", "-y", specDest}).

		// Build the binary RPM.
		WithExec([]string{"rpmbuild", "-bb", specDest}).
		WithExec([]string{"echo", fmt.Sprintf("✓ %s", specFile)}).
		Stdout(ctx)
}

// buildResult holds the outcome of a single spec file build.
type buildResult struct {
	specFile string
	output   string
	err      error
}

// BuildSpecFiles builds multiple RPM spec files in parallel, collecting all
// results before returning so every failure is reported in a single run.
//
// extraCoprRepos is forwarded to each BuildSpecFile call.
func (m *Copr) BuildSpecFiles(
	ctx context.Context,
	// repository root
	// +defaultPath="/"
	source *dagger.Directory,
	// rpm spec files to be built
	specFiles []string,
	// fedora version to build against
	// +default="43"
	fedoraVersion string,
	// additional COPR repositories to enable (optional)
	// +optional
	extraCoprRepos []string,
) (string, error) {
	var (
		wg      sync.WaitGroup
		mu      sync.Mutex
		results []buildResult
		skipped []string
	)

	for _, specFile := range specFiles {
		if !strings.HasSuffix(specFile, ".spec") {
			skipped = append(skipped, specFile)
			continue
		}

		wg.Add(1)
		go func(sf string) {
			defer wg.Done()

			output, err := m.BuildSpecFile(ctx, source, sf, fedoraVersion, extraCoprRepos)

			mu.Lock()
			results = append(results, buildResult{specFile: sf, output: output, err: err})
			mu.Unlock()
		}(specFile)
	}

	wg.Wait()

	// Aggregate outputs and errors separately so all failures are visible.
	var outputs, errs []string

	for _, r := range results {
		if r.err != nil {
			errs = append(errs, fmt.Sprintf("✗ %s: %v", r.specFile, r.err))
		} else {
			outputs = append(outputs, r.output)
		}
	}

	if len(skipped) > 0 {
		outputs = append(outputs, fmt.Sprintf("⚠ skipped (not .spec): %s", strings.Join(skipped, ", ")))
	}

	if len(errs) > 0 {
		// Return partial output alongside the combined error so callers can
		// inspect which builds succeeded before reporting failure.
		return strings.Join(outputs, "\n"), fmt.Errorf("one or more builds failed:\n%s", strings.Join(errs, "\n"))
	}

	return strings.Join(outputs, "\n"), nil
}

// BuildSpecFilesOrdered builds groups of spec files sequentially, where specs
// within each group build in parallel.
//
// This is required when specs have dependencies on each other — for example,
// ghostty/gtk4-layer-shell.spec must be built and installed before
// ghostty/ghostty.spec can resolve its build dependencies.
//
// Example call:
//
//	specGroups: [["ghostty/gtk4-layer-shell.spec"], ["ghostty/ghostty.spec"]]
//
// Each group completes fully (all specs in it succeed) before the next group
// starts. A failure in any group halts execution and returns partial output
// alongside the error.
func (m *Copr) BuildSpecFilesOrdered(
	ctx context.Context,
	// repository root
	// +defaultPath="/"
	source *dagger.Directory,
	// ordered groups of spec files; each group runs after the previous completes
	specGroups [][]string,
	// fedora version to build against
	// +default="43"
	fedoraVersion string,
	// additional COPR repositories to enable (optional)
	// +optional
	extraCoprRepos []string,
) (string, error) {
	var allOutputs []string

	for i, group := range specGroups {
		out, err := m.BuildSpecFiles(ctx, source, group, fedoraVersion, extraCoprRepos)
		// Collect output even on error so the caller sees what succeeded.
		if out != "" {
			allOutputs = append(allOutputs, out)
		}
		if err != nil {
			return strings.Join(allOutputs, "\n"),
				fmt.Errorf("group %d/%d failed: %w", i+1, len(specGroups), err)
		}
	}

	return strings.Join(allOutputs, "\n"), nil
}
