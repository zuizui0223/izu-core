#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args) >= 1) args[[1]] else "artifacts/seychelles_restoration_iwdb"
outdir <- if (length(args) >= 2) args[[2]] else file.path(root, "empirical_extracted")
files <- list.files(root, pattern = "^Empirical_data\\.RData$", recursive = TRUE, full.names = TRUE)
if (length(files) != 1) stop(sprintf("expected exactly one Empirical_data.RData, found %d", length(files)))
env <- new.env(parent = emptyenv())
loaded <- load(files[[1]], envir = env)
if (!("all_dat" %in% loaded)) stop("Empirical_data.RData does not contain all_dat")
dat <- get("all_dat", envir = env)
if (!is.data.frame(dat)) stop("all_dat is not a data.frame")
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
write.csv(dat, file.path(outdir, "all_dat.csv"), row.names = FALSE, na = "")
writeLines(c(
  paste0("source_file=", files[[1]]),
  paste0("loaded_objects=", paste(loaded, collapse = ",")),
  paste0("rows=", nrow(dat)),
  paste0("columns=", ncol(dat)),
  paste0("column_names=", paste(names(dat), collapse = ","))
), file.path(outdir, "extraction_manifest.txt"))
cat(sprintf("extracted all_dat: %d rows x %d columns\n", nrow(dat), ncol(dat)))
