.PHONY: srpm

srpm:
	@set -eu; \
	  dnf -y install rpm-build rpmdevtools rpmautospec rpmautospec-rpm-macros; \
	  sources_dir="$$(mktemp -d)"; \
	  processed_spec="$$(mktemp --suffix=.spec)"; \
	  trap 'rm -rf "$$sources_dir" "$$processed_spec"' EXIT; \
	  mkdir -p "$(outdir)"; \
	  rpmautospec process-distgit "$(spec)" "$$processed_spec"; \
	  spectool -g -C "$$sources_dir" "$$processed_spec"; \
	  rpmbuild -bs --nodeps \
	    --define "_sourcedir $$sources_dir" \
	    --define "_srcrpmdir $(outdir)" \
	    "$$processed_spec"
