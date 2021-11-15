import java.util.InputMismatchException;
import java.util.Scanner;

public class DivideByZeroWithExceptionHandling
{
   public static int quotient(int numerator, int denominator) throws ArithmeticException {
      return numerator / denominator;
   } 
 
   public static void main(String[] args) {
      Scanner scanner = new Scanner(System.in); 
      boolean continueLoop = true;
      int numerator = 0, denominator = 0;
      do {    
    	 try {
    		 System.out.print("Please enter an integer numerator: ");    
    		 numerator = scanner.nextInt();                            
    		 System.out.print("Please enter an integer denominator: ");  
    		 denominator = scanner.nextInt();     
    		 int result = quotient(numerator, denominator);              
    		 System.out.printf("%nResult: %d / %d = %d%n", numerator, denominator, result);                                     
    		 continueLoop = false;     
         } catch (InputMismatchException inputMismatchException) {        
            System.err.printf("%nException: %s%n", inputMismatchException);                                  
            scanner.nextLine();   
            System.out.printf("You must enter integers. Please try again.%n%n");          
         } catch (ArithmeticException arithmeticException) { 
        	 System.err.printf("%nException:%s Oops, can't do that.", arithmeticException);
             System.out.printf("%nZero is an invalid denominator. Please try again.%n%n"); 
         } finally { 
        	 System.out.printf("%nNumerator is %d%n", numerator);
        	 System.out.printf("Denominator is %d%n%n", denominator);
         }
      } while (continueLoop);
      
   } 
}
