
public class Triple {	
	private String[] times;	
	private int n;
	private String date;
	
	public Triple(String[] times, String date) {
		this.times = times;
		n = times.length - 1;
		this.date = date;
	}
	
	public String getTriples() {
		StringBuilder rst = new StringBuilder();
		
		for (int i = 1; i <= n; ++i) {
			rst.append(getATriple(i, date, times, n));
		}
		
		return rst.toString();
	}
	
	public String getATriple(int i, String date, String[] times, int n) {
		StringBuilder sb = new StringBuilder();
		String postfix = "_of_" + n + " ";
		sb.append("ampo:printing_layer_").append(i).append(postfix);
		int len = sb.length();
		String space = new String(new char[len]).replace('\0', ' ');
		sb.append("rdf:type ampo:Process ;\n").append(space).append("prov:startedAtTime \"");
		sb.append(date).append(times[i-1]).append("\"^^xsd:dateTime ;\n");
		sb.append(space).append("prov:endedAtTime \"");
		sb.append(date).append(times[i]).append("\"^^xsd:dateTime ;\n");

		if (i < n) {
			sb.append(space).append("ampo:happensDirectlyBefore ampo:printing_layer_").append(i+1).append(postfix).append(";\n");
		}
		
		sb.append(space).append("ampo:hasNumberOfSteps \"2\"^^xsd:int ;\n");
		sb.append(space).append("ampo:hasStep ampo:indexing_").append(i).append(postfix).append(",\n");
		space = space + new String(new char["ampo:hasStep ".length()]).replace('\0', ' ');
		sb.append(space).append("ampo:material_deposition_").append(i).append(postfix).append(".\n\n");
		
		String second = "ampo:indexing_" + i + postfix;
		sb.append(second);		
	    len = second.length();
		space = new String(new char[len]).replace('\0', ' ');
		sb.append("rdf:type ampo:Step ;\n").append(space);
		sb.append("ampo:happensDirectlyBefore ampo:material_deposition_").append(i).append(postfix).append(".\n\n");
		
		sb.append("ampo:material_deposition_").append(i).append(postfix).append("rdf:type ampo:Step .\n\n\n");
		
		return sb.toString();	
	}
}
