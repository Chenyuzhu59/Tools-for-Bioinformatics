# install necessary libraries
p <- c("xgboost","optparse","Matrix", "data.table","parallel")
usePackage <- function(p) {
  if (!is.element(p, installed.packages()[,1]))
    install.packages(p, dep=TRUE, repos="http://cran.us.r-project.org/")
  suppressWarnings(suppressMessages(invisible(require(p, character.only=TRUE))))
}
invisible(lapply(p, usePackage))

#require(optparse)
#require(xgboost)
#require(Matrix)
#require(data.table)

args <- commandArgs(trailingOnly=TRUE)
c_thread <- detectCores()
option_list <- list(
  make_option(c("-t", "--table_file"), type="character", help="Input feature table with relative abundance as traning data(*.Abd) [Required]"),
  make_option(c("-m", "--meta_data"), type="character", help="Input meta data file [Required]"),
  make_option(c("-r", "--nround"), type="integer", default=20, help="Number of round [Optional, default %default]"),
  make_option(c("-o", "--out_dir"), type="character", default='XGBoost_Model', help="Output file name[default %default]"),
  make_option(c("-n", "--nthread"), type="integer",default=c_thread, help=" Number of threads [Optional, default %default]"),
  make_option(c("-d", "--depth"), type="integer",default=3, help=" Number of max depth [Optional, default %default]")
)
opts <- parse_args(OptionParser(option_list=option_list), args=args)

matrixfile <- opts$table_file
mapfile <- opts$meta_data
outpath <- opts$out_dir
dir.create(outpath)

training <- read.table(matrixfile,row.names = 1,header = T)
trainingmap <- read.table(mapfile,row.names = 1,header = T)

setwd(outpath)
tempmatrix<-data.matrix(training)

levels_num<-nlevels(as.factor(trainingmap[,1]))
levels_name<-levels(factor(trainingmap[,1]))

value_pred<-array("None",dim=c(2))
new_labels<-array(0,dim=c(length(trainingmap[,1])))
labels<-trainingmap[,1]
for(j in 1:length(labels)){
       for(k in 1:levels_num){
             if(labels[j]==levels_name[k]) new_labels[j]=k-1
             }
      } 

num_thread <- opts$nthread
num_round <- opts$nround
max_depth <- opts$depth
training.xb <- xgboost(data=tempmatrix,label=new_labels,nrounds=num_round,objective = "multi:softmax", num_class=levels_num, nthread=num_thread, max_depth=max_depth)

xgb.save(training.xb,'xgboost.model')
