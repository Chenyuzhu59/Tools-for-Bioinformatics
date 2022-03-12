# install necessary libraries
p <- c("randomForest","optparse")
usePackage <- function(p) {
  if (!is.element(p, installed.packages()[,1]))
    install.packages(p, dep=TRUE, repos="http://cran.us.r-project.org/")
  suppressWarnings(suppressMessages(invisible(require(p, character.only=TRUE))))
}
invisible(lapply(p, usePackage))
args <- commandArgs(trailingOnly=TRUE)
option_list <- list(
  make_option(c("-t", "--table_file"), type="character", help="Input feature table with relative abundance as traning data(*.Abd) [Required]"),
  make_option(c("-i", "--test_file"), type="character", help="Input feature table with relative abundance as testing data (*.Abd) [Required]"),
  make_option(c("-m", "--meta_data"), type="character", help="Input meta data file [Required]"),
  make_option(c("-o", "--out_dir"), type="character", default='RFimportance', help="Output file name[default %default]"),
  make_option(c("-p", "--prefix"), type="character",default='Out', help="Output file prefix [Optional, default %default]")
)
opts <- parse_args(OptionParser(option_list=option_list), args=args)

matrixfile <- opts$table_file
testingfile <- opts$test_file
mapfile <- opts$meta_data
outpath <- opts$out_dir
dir.create(outpath)

training <- read.table(matrixfile,row.names = 1,header = T,sep = "\t")
trainingmap <- read.table(mapfile,row.names = 1,header = T,sep = "\t")

# hash meta
#ids <- row.names(training)
#ids_data <- data.frame(ids)

#ids <- row.names(trainingmap)
#status <- trainingmap[,1]
#meta_data <- data.frame(ids, status)

#t_meta_data <- merge(ids_data, meta_data)  

testing <- read.table(testingfile,row.names = 1,header = T,sep = "\t")
setwd(outpath)

tempframe=data.frame(training,status=as.factor(trainingmap[,1]))
training.rf <- randomForest(status ~ .,data=tempframe,importance=T,proximity=F,ntree=2000,mtry=(2 * sqrt(dim(tempframe)[2])),nodesize=100)
for (i in 1:dim(testing)[1]) {
  tempprediction <- predict(training.rf,testing[i,])
  write.table(file=opts$prefix,tempprediction,append = T,quote =F,col.names =F, sep="\t")
}
