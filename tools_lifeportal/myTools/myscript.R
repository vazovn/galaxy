## myscript.R
## for testing with Galaxy
## read and write out a file


fpc <- read.table("sometable.txt", header = TRUE, colClasses = "numeric")
save(fpc, file = "sometable.RData")
write.csv(fpc, file = "sometableout.txt",quote = FALSE)
