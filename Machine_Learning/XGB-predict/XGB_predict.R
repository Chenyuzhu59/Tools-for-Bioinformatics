# install necessary libraries
p <- c("xgboost","optparse")
usePackage <- function(p) {
  if (!is.element(p, installed.packages()[,1]))
    install.packages(p, dep=TRUE, repos="http://cran.us.r-project.org/")
  suppressWarnings(suppressMessages(invisible(require(p, character.only=TRUE))))
}
invisible(lapply(p, usePackage))

args <- commandArgs(trailingOnly=TRUE)
option_list <- list(
  make_option(c("-t", "--test_file"), type="character", help="Input feature table with relative abundance as testing data (*.Abd) [Required]"),
  make_option(c("-m", "--model_file"), type="character", help="Input model file name(*.model) [Required]"),
  make_option(c("-o", "--out_dir"), type="character", default='XBimportance', help="Output file name[default %default]"),
  make_option(c("-p", "--prefix"), type="character",default='predict.txt', help="Output file prefix [Optional, default %default]")
)
opts <- parse_args(OptionParser(option_list=option_list), args=args)

testingfile <- opts$test_file
model <- opts$model_file
outpath <- opts$out_dir

bst <- xgb.load(model)

#dir.create(outpath)

testing <- read.table(testingfile,row.names = 1,header = T)

setwd(outpath)

value_pred<-array("None",dim=c(2))
test_rowname<-row.names(testing)

for (i in 1:dim(testing)[1]) {
    value_pred[1]<-test_rowname[i]
    tempprediction <- predict(bst,data.matrix(testing[i,]))
	if (tempprediction == 0){
		value_pred[2]<-"High"
	}else{
		value_pred[2]<-"Low"
	}
	#print(tempprediction)
    #value_pred[2]<-levels_name[tempprediction+1]
    write.table(file=opts$prefix,t(value_pred),append = T,quote =F,col.names =F, row.names=F, sep="\t")
}

