#! /usr/bin/env Rscript

library('getopt')

#get options, using the spec as defined by the enclosed list.
#we read the options from the default: commandArgs(TRUE).
spec = matrix(c(
  'code', 'c', 1, "character",
  'from', 'f', 1, "character",
  'to', 't', 1, "character",
  'index', 'i', 1, "logical",
  'help', 'h', 0, "logical"

), byrow=TRUE, ncol=4)

opt = getopt(spec)

# if help was asked for print a friendly message 
# and exit with a non-zero error code
if ( !is.null(opt$help) ) {
  cat(getopt(spec, usage=TRUE))
  q(status=1)
}

library("xts")
library("zoo")
library("TTR")
library("quantmod")
library("jsonlite")
library('httr')

getDataFromRPC <- function(code, start, end, index) {
  body <- list(method='get_k_data', jsonrpc='2.0', params=list(code=code,index=index, start=start, end=end), id=0)
  response <- POST("localhost:4000", add_headers('Content-Type'='application/json'), body=body, encode = "json")
  data <- fromJSON(content(response)$result)
  result <- as.xts(data[, -1], order.by=as.Date(data$date, format='%Y-%m-%d'))
  return(result)
}


png(paste('./images/', opt$code, opt$from, opt$to, '.png', sep=''), width = 2300, height=1660)
# data = getSymbols(opt$code, from=opt$from, to=opt$to, auto.assign=FALSE)
data <- getDataFromRPC(opt$code, opt$from, opt$to, opt$index)
chartSeries(data)
addBBands()
addMACD()
addRSI()
addCCI()
dev.off()



