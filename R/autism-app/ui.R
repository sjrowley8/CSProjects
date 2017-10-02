
# This is the user-interface definition of a Shiny web application.
# Stephen Rowley
# BIO 297
# Dr. Whitworth
# http://shiny.rstudio.com
#

library(shiny)

shinyUI(
  navbarPage("",
      tabPanel("Overview",
  
        fluidPage(
          titlePanel("Autism and Increased Paternal Age Related Changes in Global Levels of Gene Expression Regulation"),
          sidebarLayout(position = "right",
                        sidebarPanel(img(src="insight-into-autism.jpg", height = 300, width = 250),
                                     helpText(a(href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3040743/", "Publication")),
                                     helpText(a(href="http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE25507", "DataSet"))),
                        mainPanel(h4("Introduction"),
                                  p("Autism is a neurodevelopmental disorder that often impacts social interaction and verbal and
                                  non-verbal communication.  Until recently, autism was understood to be solely a genetic disorder.
                                  New research has begun to suggest that in addition to genetics, other environmental factors may 
                                  play a causal role in autism."),
                                  h4("The Data"),
                                  p("Alter et al. 2011 looked at overall gene expression profiles of 146 caucasian children, 82
                                    of which were autistic with 64 others as a control.  The group of children with autism was 
                                    significantly younger than the control group (autism: mean - 5.5 years SD - 2.1; control: 
                                    mean - 7.9 SD - 2.2, p<.0001). Paternal age was similar between groups. Peripheral blood 
                                    lymphocytes were extracted and total RNA levels were isolated.  Once isolated, the RNA was 
                                    double round amplified, cleaned, and biotin-labeled using Affymetrix's GeneChip Two-Cycle 
                                    Target Labeling kit.  These gene expression microarrays covered greater than 47,000 unique
                                    RNA transcripts."),
                                  h4("The Results"),
                                  p("This experiment yielded a few different results.  It was found that overall variance in gene 
                                  expression in peripheral blood lymphocytes was decreased in children with autism.  In addition,
                                    increased paternal age is associated with decreased overall variance in gene expression levels.
                                    A few other results were found from Alter et al 2011, including Decreased variance in gene expression 
                                    is related to the down-regulation of genes involved in the regulation of transcription, and Inhibition 
                                    of transcription leads to a decreased variance in gene expression, but this information will not 
                                    be included in the proceeding graphs.")
            
                        ),
        fluid = TRUE))),
               
      tabPanel("Scatterplot",
               
        fluidPage(
  
          sidebarLayout(position = "right",
                sidebarPanel(
                  helpText("Change the appearance of this graph."),

                  selectInput("parentGender",
                              label    = "Choose a parent gender to plot",
                              choices  = c("Father", "Mother"),
                              selected = "Father"),
                  
                  checkboxInput(inputId = "autistic",
                                label   = strong("Show Austistic Gene Expression Variance"),
                                value   = TRUE),
                  
                  checkboxInput(inputId = "control",
                                label   = strong("Show Control Gene Expression Variance"),
                                value   = TRUE),
                  
                  downloadButton('downloadData'),
                
                
                  helpText("Data from NCBI Gene Expression Omnibus (GEO)")
                  
                  ),
          mainPanel(plotOutput("scatter_plot", 
                      click = "plot_click",
                      brush = brushOpts(
                        id = "plot_brush")))),
          fluidRow(
                      column(width = 6,
                      h4("Points near click"),
                      verbatimTextOutput("click_info")),
                                    
                      column(width = 6,
                      h4("Brushed points"),
                      verbatimTextOutput("brush_info"))
                      )
        )
      ),
  
  tabPanel("K-Means Clustering",
           
           fluidPage(
             
             sidebarLayout(position = "right",
                           sidebarPanel(
                             helpText("Change the appearance of this graph."),
                             
                             numericInput('sample_num', 'Sample Number', 1,
                                          min = 1, max = 146),
                           
                           numericInput('cluster_num', 'Cluster Number', 2,
                                        min = 1, max = 9)),
                             
                          mainPanel(
                            plotOutput("cluster_plot")
                            
                          )),
           fluidRow(
              column(width=6,
                     h4("Determining number of clusters k:"),
                     plotOutput("k_plot")),
              column(width=6,
                     h4("Works Cited"),
                     p("http://www.mattpeeples.net/kmeans.html"),
                     p("http://www.r-bloggers.com/bot-botany-k-means-and-ggplot2/"),
                     p("http://shiny.rstudio.com/gallery/"))
           )
           
           
           
           
  ))))

