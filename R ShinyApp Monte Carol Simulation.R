##Problem1
DM=Workloads$`Documents to Mail`
workload = function(x){
  return(max(tapply(DM,round(x),sum)))
}
##Problem2
z=list(NULL)
wl=numeric(1000)
repeat{
  for (i in 1:1000){
    z[[i]]=runif(16,min=1,max=6)
    wl[i]=workload(z[[i]])
  }
  print(min(wl))
  print(z[[which.min(wl)]])
  k=which.min(wl)
  if (wl[k] < 390000){break}
}
##Problem3
ui = fluidPage(
titlePanel("Workload Optimization"),
hr(),
hr(),
sliderInput("NoWeeks",label="Select Number of Weeks", min=4,max=12, value=6, step=1),
sliderInput("TLoad",label="Select Target Workload", min=100000,max=1000000, value=390000, step=10000),
hr(),
verbatimTextOutput("Workload")
)
server = function(input, output) {
  output$Workload = renderText({
    z=list(NULL)
    wl=numeric(1000)
    c = 0
    repeat{
      c=c + 1
      for (i in 1:1000){
        z[[i]]=runif(16,min=1,max=input$NoWeeks)
        wl[i]=workload(z[[i]])
      }
      k=which.min(wl)
      if ((wl[k] < input$TLoad)||(c >= 10)){break}
    }
    paste0("Recommended assignment is ", paste(round(z[[k]]),collapse = ","), " with workload of ", wl[k])
    })
  }
  shinyApp(ui, server)