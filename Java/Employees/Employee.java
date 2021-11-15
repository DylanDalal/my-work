// Fig. 10.4: Employee.java
// Employee abstract superclass.

public abstract class Employee {
   private Date birthDate;
   private final String firstName;
   private final String lastName;
   private final String socialSecurityNumber;

   // constructor
   public Employee(String firstName, String lastName, 
      String socialSecurityNumber, int m, int d, int y) {
      this.firstName = firstName;
      this.lastName = lastName;
      this.socialSecurityNumber = socialSecurityNumber;
      this.birthDate = new Date(m, d, y);
   } 

   // return first name
   public String getFirstName() {return firstName;}

   // return last name
   public String getLastName() {return lastName;}

   // return social security number
   public String getSocialSecurityNumber() {return socialSecurityNumber;}

   public String getBirthDate() {
	  return String.format("%d/%d/%d", birthDate.getMonth(), birthDate.getDay(), birthDate.getYear());
   }
   
   public int getBirthMonth() {
	   return birthDate.getMonth();
   }
   
   // return String representation of Employee object
   @Override
   public String toString() {
      return String.format("%s %s%nsocial security number: %s%nbirthday: %s", 
         getFirstName(), getLastName(), getSocialSecurityNumber(), getBirthDate());
   }

   // abstract method must be overridden by concrete subclasses
   public abstract double earnings(); // no implementation here
} 