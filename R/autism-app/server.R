
# This is the server logic for a Shiny web application.
# Stephen Rowley
# BIO 297
# Dr. Whitworth
# 
# http://shiny.rstudio.com
#
library(shiny)
library(ggplot2)
library(tidyr)

shinyServer(function(input, output) {
  
  autismTable <- readRDS("table.RDS")
  scatterTable <- autismTable[, c("sampleAge", "paternalAge", "maternalAge", "standardVariance")]
  clusterTable <- autismTable[5:20000] #full dataset is 5:54617
  lm_eqn <- function(m) {
    summary <- summary(m)
    p        <- format(round(summary$coefficients[2,4],3),nsmall=3)
    rsquared <- format(round(summary$adj.r.squared,3),nsmall=3)
    pval     <- paste("P-value: ", p, sep = "")
    rsq      <- paste("R2: ", rsquared, sep="")
    string   <- paste(pval, rsq, sep = ", ")
  }
  
  
  df          <- data.frame()

  #standardVariance <- scale(variance)
  output$scatter_plot <- renderPlot({
  #to filter rows -> index on a conditional ex. autismTable[autismTable$PaternalAge >= 31,] 
    
  
  output$click_info <- renderPrint({
    #click points
    nearPoints(scatterTable, input$plot_click, addDist = TRUE)
  })
  
  output$brush_info <- renderPrint({
    # brush points
    brushedPoints(scatterTable, input$plot_brush)
  })
  
  output$downloadData <- downloadHandler(
    #download button allows downloading of brushed subset
    filename = function() { paste("autismTableSubset", '.csv', sep='') },
    content = function(file) {
      write.csv(brushedPoints(scatterTable,input$plot_brush), file)
    }
  )
    if (input$parentGender == "Father") {
      if (input$autistic && input$control) {
        regression  <- lm(scatterTable$paternalAge ~ scatterTable$standardVariance)
        lmData      <- lm_eqn(regression)
        ggplot(scatterTable, aes(paternalAge, standardVariance), alpha=0.5) + xlab("Paternal Age") + 
        ylab("Overall Gene Expression Variance") + ggtitle("Overall Gene Expression Variance vs. Paternal Age") +
        geom_point(colour="black") + geom_smooth(method = lm) + geom_text(x = 45, y = 2, label = I(lmData))
                                                                                          
        
       
     } else if (input$control) { 
       regression  <- lm(scatterTable$paternalAge[1:64] ~ scatterTable$standardVariance[1:64])
       lmData      <- lm_eqn(regression)
        ggplot(scatterTable[1:64,], aes(paternalAge, standardVariance), alpha=0.5) + xlab("Paternal Age") + 
        ylab("Overall Gene Expression Variance") + ggtitle("Overall Gene Expression Variance vs. Paternal Age") +
         geom_point(colour="black")+ geom_smooth(method = lm) + geom_text(x = 37, y = 2, label = I(lmData))

     } else if (input$autistic) {
       regression  <- lm(scatterTable$paternalAge[65:146] ~ scatterTable$standardVariance[65:146])
       lmData      <- lm_eqn(regression)
       ggplot(scatterTable[65:146,], aes(paternalAge, standardVariance), alpha=0.5) + xlab("Paternal Age") + 
        ylab("Overall Gene Expression Variance") + ggtitle("Overall Gene Expression Variance vs. Paternal Age") +
         geom_point(colour="black") + geom_smooth(method = lm)  + geom_text(x = 45, y = 2, label = I(lmData))
     }
      else {
        ggplot(df) + geom_point() + xlim(0, 10) + ylim(0, 100)
      }
    } else {
        if (input$control && input$autistic) {
          regression  <- lm(scatterTable$maternalAge ~ scatterTable$standardVariance)
          lmData      <- lm_eqn(regression)
          ggplot(scatterTable, aes(maternalAge, standardVariance), alpha=0.5) + xlab("Maternal Age") + 
          ylab("Overall Gene Expression Variance") + ggtitle("Overall Gene Expression Variance vs. Maternal Age") +
            geom_point(colour="black") + geom_smooth(method = lm) + geom_text(x = 37, y = 2, label = I(lmData))
      } else if (input$control) { 
          regression  <- lm(scatterTable$maternalAge[1:64] ~ scatterTable$standardVariance[1:64])
          lmData      <- lm_eqn(regression)
          ggplot(scatterTable[1:64,], aes(maternalAge, standardVariance), alpha=0.5) + xlab("Maternal Age") + 
          ylab("Overall Gene Expression Variance") + ggtitle("Overall Gene Expression Variance vs. Maternal Age") +
          geom_point(colour="black") + geom_smooth(method = lm)+ geom_text(x = 36, y = 2, label = I(lmData))

      } else if (input$autistic) {
          regression  <- lm(scatterTable$maternalAge[65:146] ~ scatterTable$standardVariance[65:146])
          lmData      <- lm_eqn(regression)
          ggplot(scatterTable[65:146,], aes(maternalAge, standardVariance), alpha=0.5) + xlab("Maternal Age") + 
          ylab("Overall Gene Expression Variance") + ggtitle("Overall Gene Expression Variance vs. Maternal Age") +
          geom_point(colour="black") + geom_smooth(method = lm) + geom_text(x = 37, y = 2, label = I(lmData))
      } else {
        ggplot(df) + geom_point() + xlim(0, 10) + ylim(0, 100)
      
      }
    }
  })
      
  output$cluster_plot <- renderPlot({
    
    #reformat, just 1 sample at a time
    clusterSampleTable <- gather(clusterTable[input$sample_num,],
                                 key   ="gene",
                                 value ="signal_intensity")
    clusterMatrix <- na.omit(t(as.matrix(clusterTable[input$sample_num,])))
    kmeansResults <- kmeans(clusterMatrix, input$cluster_num)
    
    #add cluster vector to table
    clusterSampleTable$cluster <- factor(kmeansResults$cluster)
    
    
    ggplot(clusterSampleTable, aes(x=gene,y=signal_intensity, color=cluster )) + geom_point()
    
    
    
  })

  
  output$k_plot <- renderPlot({
    
    
    clusterMatrix <- t(as.matrix(clusterTable[1,]))
    wss <- (nrow(clusterMatrix)-1)*sum(apply(clusterMatrix,2,var))
    for (i in 2:15) wss[i] <- sum(kmeans(clusterMatrix,
                                         centers=i)$withinss)
    plot(1:15, wss, type="b", xlab="Number of Clusters",
         ylab="Within groups sum of squares")
  })
     
    
    
})  
  
  
