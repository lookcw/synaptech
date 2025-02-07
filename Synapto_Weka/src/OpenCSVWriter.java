import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

import au.com.bytecode.opencsv.CSVReader;
import au.com.bytecode.opencsv.CSVWriter;
import weka.classifiers.AbstractClassifier;
import weka.classifiers.Classifier;
import weka.classifiers.evaluation.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import weka.core.Utils;
import weka.core.converters.CSVLoader;

public class OpenCSVWriter {
	
	public static void headerWriter(CSVWriter writer) throws Exception {
		
		 String [] labels = "Date,Filename,Num Seeds,TP,TN,FP,FN,F-measure,AUC,Classifier,Classifer Parameters".split(",");	        
		 writer.writeNext(labels);

	}

	/* Automatically runs classifier on 10 seeds */
	public static void mainWriter(String CSVFilePath, int folds, int numSeeds, CSVWriter writer) throws Exception {
	
		double tp = 0.0, tn = 0.0, fp = 0.0, fn = 0.0, fmeasure = 0.0, auc = 0.0;
		String filename = null, classifier = null, classifier_para = null;
		CSVLoader loader = new CSVLoader();
		loader.setSource(new File(CSVFilePath));
	
	   String[] options = new String[1]; 
	   options[0] = "";
	   // -H means no header
	   loader.setOptions(options);
	   
       /* Getting values for number of seeds specified - (random values) */
	   for(int i = 0; i < numSeeds; i++) {

		   Instances data = loader.getDataSet();
		   Random rand = new Random(i);   // create seeded number generator - get 10 random nums
		   Instances randData = new Instances(data);   // create copy of original data
		   randData.randomize(rand);         // randomize data with number generator
		   RandomForest rf = new RandomForest();
		           
		   
		  randData.setClassIndex(randData.numAttributes() - 1);
		   
		    Evaluation eval = new Evaluation(randData);
		    
		    for (int n = 0; n < folds; n++) {
		         Instances train = randData.trainCV(folds, n);
		         Instances test = randData.testCV(folds, n);
		         // the above code is used by the StratifiedRemoveFolds filter, the
		         // code below by the Explorer/Experimenter:
		         // Instances train = randData.trainCV(folds, n, rand);
		 
		         // build and evaluate classifier
		         Classifier clsCopy = AbstractClassifier.makeCopy(rf);
		         clsCopy.buildClassifier(train);
		         eval.evaluateModel(clsCopy, test);
		         
	
		    }
		    	  
		    /* To get average across number of seeds */
		    tp += eval.weightedTruePositiveRate();
		    tn += eval.weightedTrueNegativeRate();
		    fp += eval.weightedFalsePositiveRate();
		    fn += eval.weightedFalseNegativeRate();
		    fmeasure += eval.weightedFMeasure();
		    auc += eval.weightedAreaUnderROC();
	                
		    filename = data.relationName();
		    classifier = rf.getClass().getName();
		    classifier_para = Utils.joinOptions(rf.getOptions());
	        
		}
	   /* Get averages */
	   tp /= numSeeds;
	   tn /= numSeeds;
	   fp /= numSeeds;
	   fn /= numSeeds;
	   fmeasure /= numSeeds;
	   auc /= numSeeds;
	   
	   System.out.println(filename);
	   System.out.println(classifier);
	   System.out.println(classifier_para);
	   System.out.println("TP: " + tp + " TN: " + tn + 
			   " FP: " + fp + " FN: " + fn + " Fmeasure " + fmeasure + " AUC: " + auc);
	   
	   /* Get today's date */
	   DateTimeFormatter dtf = DateTimeFormatter.ofPattern("MM/dd/yyyy");  
	   LocalDateTime now = LocalDateTime.now();  
	   
	   String[] nums =  {dtf.format(now), filename, Integer.toString(numSeeds), 
			   String.format("%.2f",  tp), 
			   String.format("%.2f",  tn),
			   String.format("%.2f",  fp),
			   String.format("%.2f",  fn),
			   String.format("%.2f",  fmeasure),
			   String.format("%.2f",  auc), classifier, classifier_para};
	 
	   
	   writer.writeNext(nums);
	   	 
	}
	
	public static boolean isInteger(String s) {
	    try { 
	        Integer.parseInt(s); 
	    } catch(NumberFormatException e) { 
	        return false; 
	    } catch(NullPointerException e) {
	        return false;
	    }
	    // only got here if we didn't return false
	    return true;
	}
	        
	public static void main(String[] args) throws Exception {
		
		/* Input path is the file where you are reading from and output filename is the name of the
		 * file that you want to output results into */
		String input_path = "", output_filename = "default_file.csv";
		int numFolds = 10, numSeeds = 10;
		
		/* Setting input and output files */
		if(args[0].equals("-i") && args[2].equals("-o")) {
			input_path = args[1];
			output_filename = args[3];
		} else if(args[0].equals("-o") && args[2].equals("-i")) {
			input_path = args[3];
			output_filename = args[1];
		} else {
			System.out.println("Did not enter an input filepath and/or output file");
			return;
		}
		
		
		CSVWriter writer = new CSVWriter(new FileWriter(output_filename, true));
		CSVReader reader = new CSVReader(new FileReader(output_filename));
		
		String[] header;
		/* Make sure that header is only written once */
		if((header = reader.readNext()) == null) {
			headerWriter(writer);
		} 	
		
		mainWriter(input_path, numFolds, numSeeds, writer);
		
		/*mainWriter("../../Synapto/tensorflow/Brazil/Feature_Sets/Fil_higARmin7.csv", 
				10, 10, writer);*/
	
		writer.close();
	}

}
