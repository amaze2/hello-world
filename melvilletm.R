
library(XML)
inputDir <- "data/XML1"
files.v <- dir(path = inputDir, pattern=".*xml")
chunk.size <- 1000 #number of words per chunk

makeFlexTextChunks <- function(doc.object, chunk.size=10, percentage=TRUE){
  paras <-getNodeSet(doc.object, 
                     "/d:TEI/d:text/d:body//d:p",
                     c(d = "http://www.tei-c.org/ns/1.0"))
  words <- paste(sapply(paras, xmlValue), collapse = " ")
  words.lower <- tolower(words)
  words.lower <- gsub("[^[:alnum:][:space:]']", " ", words.lower)
  words.l <- strsplit(words.lower, "\\s+")
  word.v <- unlist(words.l)
  x <- seq_along(word.v)
  if(percentage) {
    max.length <- length(word.v)/chunk.size
    chunks.l <- split(word.v, ceiling(x/max.length))
  } else{
    chunks.l <- split(word.v, ceiling(x/chunk.size))
    if(length(chunks.l[[length(chunks.l)]]) <= chunk.size/2){
      chunks.l[[length(chunks.l)-1]] <- c(chunks.l[[length(chunks.l)-1]],
                                          chunks.l[[length(chunks.l)]])
      chunks.l[[length(chunks.l)]] <- NULL
    }
  }
  chunks.l <- lapply(chunks.l, paste, collapse=" ")
  chunks.df <- do.call(rbind, chunks.l)
  return(chunks.df)
}

topic.m <- NULL
for(i in 1:length(files.v)){
  doc.object <- xmlTreeParse(file.path(inputDir, files.v[1]),
                             useInternalNodes = TRUE)
  chunk.m <- makeFlexTextChunks(doc.object, chunk.size, percentage = FALSE)
  textname <- gsub("\\..*","", files.v[1])
  segments.m <- cbind(paste(textname, 
                            segment=1:nrow(chunk.m), sep="_"), chunk.m)
  topic.m <-rbind(topic.m, segments.m)
}
documents <- as.data.frame(topic.m, stringsAsFactors=F)
colnames(documents) <- c("id", "text")

install.packages("mallet")
library(mallet)

mallet.instances <- mallet.import(documents$id, 
                                  documents$text,
                                  "data/stoplist.csv",
                                  FALSE,
                                  token.regexp="[\\p{L}']+")

topic.model <- MalletLDA(num.topics = 43)
topic.model$loadDocuments(mallet.instances)

vocabulary<-topic.model$getVocabulary()
class(vocabulary)
length(vocabulary)

word.freqs <- mallet.word.freqs(topic.model)
head(word.freqs)

topic.model$train(400)

topic.words.m <- mallet.topic.words(topic.model, 
                                    smoothed = TRUE,
                                    normalized = TRUE)
dim(topic.words.m)
rowSums(topic.words.m)
topic.words.m[1:3, 1:3]
vocabulary<-topic.model$getVocabulary()
colnames(topic.words.m) <- vocabulary
topic.words.m[1:3, 1:3]

keywords <- c("whale", "ship")
topic.words.m[, keywords]

imp.row<-which(rowSums(topic.words.m[, keywords]) ==
                 max(rowSums(topic.words.m[, keywords])))

mallet.top.words(topic.model, topic.words.m[imp.row,], 10)

install.packages("wordcloud")
library(wordcloud)
topic.top.words<-mallet.top.words(topic.model,
                                  topic.words.m[imp.row,], 100)
wordcloud(topic.top.words$words, 
          topic.top.words$weights,
          c(4,.8), rot.per=0, random.order = F)
