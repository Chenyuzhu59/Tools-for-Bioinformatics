# Function: PCA Monte-Carlo test
# Call: Rscript PCA_MC_test.R -i test.pc -c control.pc -o output.txt
# R packages used: ade4

## install necessary libraries
.libPaths("~/R/x86_64-pc-linux-gnu-library/3.6")
p <- c("optparse", "ade4")
usePackage <- function(p) {
  if (!is.element(p, installed.packages()[,1]))
    install.packages(p, dep=TRUE, repos="http://cran.us.r-project.org/")
  suppressWarnings(suppressMessages(invisible(require(p, character.only=TRUE))))
}
invisible(lapply(p, usePackage))

## clean R environment
## rm(list = ls())
## setwd('./')

## parsing arguments
args <- commandArgs(trailingOnly=TRUE)

# make option list and parse command line
option_list <- list(
  make_option(c("-i", "--input_abd_file"), type="character", help="Input .pc file [Required]."),
  make_option(c("-c", "--control_abd_file"), type="character", help="Control.pc file [Required]."),
  make_option(c("-o", "--outfile"), type="character", default='pc_mc_test.txt', help="Output file [default %default].")  
)
opts <- parse_args(OptionParser(option_list=option_list), args=args)

# paramenter checking
if(is.null(opts$input_abd_file)) stop('Please supply an input .pc table.')
if(is.null(opts$control_abd_file)) stop('Please supply a control .pc table.')

# load data
pca1=read.table(file=opts$input_abd_file, header=T, row.names=1, sep="\t")
pca2=read.table(file=opts$control_abd_file, header=T, row.names=1, sep="\t")

# calculation

pc1 <-data.frame(pca1)
pc2 <-data.frame(pca2)
ppa <- procuste.randtest( pc1, pc2, 10000)

con <- file(opts$outfile)
sink(con, append = TRUE)
print(ppa)
sink()
