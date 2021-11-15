public class PieceWorker extends Employee {
	private double wage;
	private double pieces;
	
	public PieceWorker(String first, String last, String ssn, 
			int m, int d, int y, double w, double p) {
		super(first, last, ssn, m, d, y);
		wage = w;
		pieces = p;
	}
	
	public void setWage(double w) { wage = w; }
	
	public void setPieces(double p) { pieces = p; }

	
	@Override                                                           
	public double earnings() {                                          
		 return pieces * wage;                                                               
	}
	
	@Override
	   public String toString() {
	      return String.format("pieceworker employee: %s %s%nsocial security number: %s%nbirthday: %s%nwage: $%.2f; pieces: %.0f%n", 
	         getFirstName(), getLastName(), getSocialSecurityNumber(), getBirthDate(), wage, pieces);
	   }
}
