import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        String srcDirPath = "src/";

        try (Stream<Path> paths = Files.walk(Paths.get(srcDirPath))) {
            paths.filter(Files::isRegularFile)
                    .filter(path -> path.toString().endsWith(".vtt"))
                    .forEach(Main::convertVttToSrt);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void convertVttToSrt(Path vttPath) {
        try {
            String inputFilePath = vttPath.toString();
            // 替换扩展名为 .srt
            String outputFilePath = inputFilePath.substring(0, inputFilePath.lastIndexOf('.')) + ".srt";

            BufferedReader br = new BufferedReader(new FileReader(inputFilePath));
            BufferedWriter bw = new BufferedWriter(new FileWriter(outputFilePath));
            String line;
            StringBuilder result = new StringBuilder();
            int i = 1;
            while ((line = br.readLine()) != null) {
                if (line.startsWith("0")) {
                    line = line.replace('.', ','); // 替换行内的所有 . 为 ,
                    if (i != 1) { // 如果不是第一个数字，添加一个空白行
                        result.append("\n");
                    }
                    result.append(i).append("\n").append(line);
                    i++;
                } else {
                    result.append("\n").append(line).append("\n");
                }
            }

            // 将结果写入新文件
            bw.write(result.toString());
            bw.close(); // 关闭 BufferedWriter
            br.close(); // 关闭 BufferedReader

            System.out.println("已将 " + inputFilePath + " 转换为：" + outputFilePath);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}