import java.io.*;
import org.apache.commons.io.FileUtils;

public class AddLabel {

    public static void main(String[] args) {
        File f = new File("FDM_data.ttl");
        File file = new File("new.ttl");
        StringBuffer sb = new StringBuffer();

        try (BufferedReader br = new BufferedReader(new FileReader(f))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.length() >= 5 && line.substring(0, 5).equals("ampo:")) {
                    String[] strs = line.split(" ");
                    int len = strs[0].length();
                    String space = new String(new char[len + 1]).replace('\0', ' ');
                    String item = strs[0].substring(5);
                    item = String.join(" ", item.split("_"));
                    sb.append(strs[0]).append(" rdfs:label \"").append(item).append("\" ;").append("\n");
                    sb.append(space).append(line.substring(len + 1)).append("\n");

                } else {
                    sb.append(line).append("\n");
                }


            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println(sb.toString());

        //FileUtils.writeStringToFile(file, sb.toString());

    }
}