import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

public class TripleGenerator {	

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		String[] times = {
				"13:32:53.4", 
				"13:33:03.4", 
				"13:33:13.2", 
				"13:33:24.0", 
				"13:33:34.5", 
				"13:33:45.3", 
				"13:33:55.8", 
				"13:34:06.6", 
				"13:34:17.2", 
				"13:34:27.9", 
				"13:34:38.5", 
				"13:34:49.2", 
				"13:34:59.8", 
				"13:35:10.5", 
				"13:35:21.2", 
				"13:35:31.9", 
				"13:35:42.5", 
				"13:35:53.2", 
				"13:36:03.8", 
				"13:36:14.5", 
				"13:36:25.1", 
				"13:36:35.8", 
				"13:36:46.4", 
				"13:36:57.1", 
				"13:37:07.8", 
				"13:37:18.5", 
				"13:37:29.1", 
				"13:37:39.8", 
				"13:37:50.4", 
				"13:38:01.1", 
				"13:38:11.7", 
				"13:38:22.4", 
				"13:38:33.5", 
				"13:38:44.4"};	
		String date = "2016-05-10T";
		
		Triple triple = new Triple(times, date);
		BufferedWriter writer = new BufferedWriter(new FileWriter("process_triples.ttl"));
		writer.write(triple.getTriples());
		writer.close();
	}
}
