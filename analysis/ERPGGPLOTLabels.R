library(reshape2)
library(lattice)
library(ggplot2)

setwd("/Users/bastienboutonnet/Google Drive/3. Current Projects/ERP_Lupyan Exps/LabelsERP")

read.table('14GavGraphExport.txt', header=TRUE) -> data

#Subest data by time
data <- subset(data, time<801)

#RESHAPE & RE-ORDER CONDITION LIST FOR MORE INTUITIVE ORDER
new.data <- melt(data, id.var = c("Condition","time"), variable.name="ROI", value.name="Amplitude")
new.data <- transform(new.data, Condition=factor(Condition, levels=c("Label", "Sound","Match", "Mismatch")))
new.dataCue <- subset(new.data, Condition==c("Label","Sound"))


#STANDARDISED STYLE FOR GRAPHS (WHATEVER I LIKE AT THE MINUTE)
##############################################################
#PimpMyPlot <- theme_bw() + theme(axis.text = element_text(color = "grey35"), panel.grid.major.y = element_line(color = "grey72", size = 0.5), panel.grid.minor.y = element_line(size = 0.2, color = "grey72"), strip.background = element_rect( fill = "grey89"), panel.border = element_rect(colour="NA"), legend.key = element_rect(color = "white"), legend.background = element_rect(colour="grey72", size=0.5))
PimpMyPlot <- theme(text=element_text(size=12,family="Palatino"))+
  theme(axis.line=element_line(colour='black'))+
  theme(axis.line.y=element_blank())+
  theme(axis.text=element_text(colour="black"))+
  theme(panel.grid.major.y=element_line(linetype='dotted',colour='grey50',size=0.3))+
  theme(panel.background=element_rect(fill="grey97"))

#plot data:
erpplot <- ggplot(new.dataCue, aes(x=time,y=Amplitude))
erpplot+labs(x ="Time (ms)",y="Amplitude (µV)")+ 
  ylim(-5.5,9)+ 
  xlim(-100,800)+ 
  geom_vline(xintercept=0,colour="black",size=0.3)+
  geom_hline(yintercept=0,colour="black",size=0.3)+ 
  geom_ribbon(aes(ymin=Amplitude-1,ymax=Amplitude+1,fill=Condition,colour=Condition),linetype=2,alpha=0.1,size=0.1)+
  geom_line(aes(colour=Condition), size=0.3)+
  scale_colour_brewer(palette="Set1")+
  scale_fill_brewer(palette="Set1")+
  facet_wrap(~ROI)+PimpMyPlot

#SOME SHIT I MIGHT WANT TO DO ONE DAY
#####################################
#create and scale timepoints:
#daten$Zeit <- rep(1:512, length(cond.list))
#daten$Zeit <- (daten$Zeit*2)-200

# delete auxiliary channels:
#tmp <- subset(new.daten, Elektrode != "M1" & Elektrode != "M2" & Elektrode != "HEOG"& Elektrode != "VEOG")

# reorder electrodes for better readability in plot:
#tmp$Elektrode<-factor(tmp$Elektrode,levels=c("Fp1","Fpz","Fp2","AF7","AF3","AF4","AF8","F7","F5","F3","F1","Fz","F2","F4","F6","F8","FT7","FC5","FC3","FC1","FCz","FC2","FC4","FC6","FT8","T7","C5","C3","C1","Cz","C2","C4","C6","T8","TP7","CP5","CP3","CP1","CPz","CP2","CP4","CP6","TP8","P7","P5","P3","P1","Pz","P2","P4","P6","P8","PO7","PO5","PO3","POz","PO4","PO6","PO8","O1","Oz","O2"))
