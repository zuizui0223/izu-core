args <- commandArgs(trailingOnly = TRUE)
out <- if (length(args) >= 1) args[[1]] else "data/results/dore2021_frozen_structure_source.csv"
target_path <- if (length(args) >= 2) args[[2]] else "data/results/frozen_dore_network_targets.csv"

# Doré et al. structure models use the full-pollinator, structure-filtered,
# non-polar source table, not the unfiltered aggregate table.
url <- "https://raw.githubusercontent.com/MaelDore/Pollination_networks/master/Data/Filtered_Datasets/aggreg.webs_full_str_no_polar.RData"
tmp <- tempfile(fileext = ".RData")
download.file(url, tmp, mode = "wb", quiet = TRUE)
x <- readRDS(tmp)
targets <- read.csv(target_path, stringsAsFactors = FALSE, check.names = FALSE)

# Use the source-native transformed covariates actually named in Doré's
# topology formulas. Do not reconstruct ln_* columns locally.
required <- c(
  "Region_pub", "Connectance", "Li", "Lp",
  "ln_sptot", "ln_pl", "ln_ins", "ln_SE", "ln_ATS", "Sampling_type"
)
missing <- setdiff(required, names(x))
if (length(missing) > 0) {
  stop(paste("Missing required source columns:", paste(missing, collapse = ", ")))
}

keep <- x[x$Region_pub %in% targets$region_pub, , drop = FALSE]
if (nrow(keep) == 0) stop("No frozen target rows found in source RDS")

cols <- unique(c(
  "Region_pub", "Location", "Country_location", "Land_type",
  "Connectance", "Li", "Lp", "full_insects", "full_plants", "sptot", "interactions",
  "Sampling_effort", "Sampling_time", "Annual_time_span", "Sampling_type",
  "ln_sptot", "ln_pl", "ln_ins", "ln_SE", "ln_time", "ln_ATS",
  "Latitude_dec", "Longitude_dec"
))
cols <- cols[cols %in% names(keep)]
keep <- keep[, cols, drop = FALSE]

# Preserve source order; Python joins to the frozen registry by Region_pub.
dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
write.csv(keep, out, row.names = FALSE, na = "")

cat("source_file", "aggreg.webs_full_str_no_polar.RData", "\n")
cat("source_rows", nrow(x), "\n")
cat("frozen_rows", nrow(keep), "\n")
cat("columns", paste(names(keep), collapse = "|"), "\n")
cat("region_ids", paste(keep$Region_pub, collapse = "|"), "\n")
