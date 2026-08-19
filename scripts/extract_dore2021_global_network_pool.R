args <- commandArgs(trailingOnly = TRUE)
raw_path <- if (length(args) >= 1) args[[1]] else "data/external/dore2021/aggreg.webs_full.RData"
out_path <- if (length(args) >= 2) args[[2]] else "data/external/dore2021/aggreg.webs_full.csv"
url <- "https://raw.githubusercontent.com/MaelDore/Pollination_networks/master/Data/Filtered_Datasets/aggreg.webs_full.RData"

dir.create(dirname(raw_path), recursive = TRUE, showWarnings = FALSE)
if (!file.exists(raw_path)) {
  download.file(url, raw_path, mode = "wb", quiet = TRUE)
}

env <- new.env(parent = emptyenv())
loaded <- load(raw_path, envir = env)
objs <- mget(loaded, envir = env)
is_df <- vapply(objs, is.data.frame, logical(1))
if (!any(is_df)) stop("No data.frame object found in Dore RData")
dfs <- objs[is_df]
sizes <- vapply(dfs, nrow, integer(1))
chosen_name <- names(which.max(sizes))
df <- dfs[[chosen_name]]

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
write.csv(df, out_path, row.names = FALSE, fileEncoding = "UTF-8")
cat("loaded_objects:", paste(loaded, collapse=","), "\n")
cat("chosen_object:", chosen_name, "rows:", nrow(df), "cols:", ncol(df), "\n")
cat("columns:", paste(names(df), collapse="|"), "\n")
