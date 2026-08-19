args <- commandArgs(trailingOnly = TRUE)
raw_path <- if (length(args) >= 1) args[[1]] else "data/external/dore2021/aggreg.webs_full.RData"
out_path <- if (length(args) >= 2) args[[2]] else "data/external/dore2021/aggreg.webs_full.csv"
url <- "https://raw.githubusercontent.com/MaelDore/Pollination_networks/master/Data/Filtered_Datasets/aggreg.webs_full.RData"

dir.create(dirname(raw_path), recursive = TRUE, showWarnings = FALSE)
if (!file.exists(raw_path)) {
  download.file(url, raw_path, mode = "wb", quiet = TRUE)
}

# Despite the .RData suffix, this source file is a single serialized R object
# (gzip-compressed XDR; readRDS-compatible), not a multi-object save() workspace.
obj <- readRDS(raw_path)
if (!is.data.frame(obj)) stop("Dore serialized object is not a data.frame")
df <- obj

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
write.csv(df, out_path, row.names = FALSE, fileEncoding = "UTF-8")
cat("serialization: readRDS\n")
cat("rows:", nrow(df), "cols:", ncol(df), "\n")
cat("columns:", paste(names(df), collapse="|"), "\n")
