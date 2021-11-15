public class PayrollSystemTest {
   public static void main(String[] args) {
	  int CURRENT_MONTH = 12;
	  String[] months = {"", "January", "February", "March", "April", "May", "June", "July",
			  	"August", "September", "October", "November", "December"};

	  SalariedEmployee salariedEmployee =                                 
         new SalariedEmployee("John", "Smith", "111-11-1111", 12, 1, 1988, 800.00);    
      HourlyEmployee hourlyEmployee =                                     
         new HourlyEmployee("Karen", "Price", "222-22-2222", 12, 4, 1985, 16.75, 40);  
      CommissionEmployee commissionEmployee =                             
         new CommissionEmployee(                                          
         "Sue", "Jones", "333-33-3333", 2, 4, 1999, 10000, .06);                      
      BasePlusCommissionEmployee basePlusCommissionEmployee =             
         new BasePlusCommissionEmployee(                                  
         "Maddy", "Reinhart", "444-44-4444", 11, 19, 2000, 5000, .04, 300);                  
      PieceWorker pieceWorker = new PieceWorker(
    		  "Bob", "Stevens", "143-14-1923", 11, 23, 1983, 14.5, 100);
      
      Employee[] employees = new Employee[5]; 
      
      employees[0] = salariedEmployee;          
      employees[1] = hourlyEmployee;            
      employees[2] = commissionEmployee;        
      employees[3] = basePlusCommissionEmployee;
      employees[4] = pieceWorker;
      
      System.out.printf("Month is currently set to " + months[CURRENT_MONTH] + ".%n");
      System.out.printf("Employees processed polymorphically:%n%n");
      
      for (Employee currentEmployee : employees) {
         System.out.println(currentEmployee);
         if (currentEmployee.getBirthMonth() != CURRENT_MONTH)
        	 System.out.printf("earned $%,.2f%n%n", currentEmployee.earnings());
         else {
        	 System.out.printf(
        			 "earned $%,.2f, including the Birthday Bonus.%n%n", (currentEmployee.earnings() + 100));
         }
      }    
   } 
} 
