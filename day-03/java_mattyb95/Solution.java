import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Solution {

    // Day 3: Mull It Over

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        StringBuilder string = new StringBuilder();
        while (scanner.hasNextLine()) {
            string.append(scanner.nextLine());
        }

        // Part 1
        System.out.println(partOne(string.toString()));

        // Part 2
        System.out.println(partTwo(string.toString()));
    }

    private static int partOne(String string) {
        String regex = "mul\\((\\d{1,3}),(\\d{1,3})\\)";
        Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE);
        Matcher matcher = pattern.matcher(string);
        int result = 0;
        while (matcher.find()) {
            int a = Integer.parseInt(matcher.group(1));
            int b = Integer.parseInt(matcher.group(2));
            result += a * b;
        }
        return result;
    }

    private static int partTwo(String string) {
        String regex = "do\\(\\)|don't\\(\\)|mul\\((\\d{1,3}),(\\d{1,3})\\)";
        Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE);
        Matcher matcher = pattern.matcher(string);
        boolean isEnabled = true;
        int result = 0;
        while (matcher.find()) {
            switch (matcher.group(0)) {
                case "do()" -> isEnabled = true;
                case "don't()" -> isEnabled = false;
                default -> {
                    if (isEnabled) {
                        int a = Integer.parseInt(matcher.group(1));
                        int b = Integer.parseInt(matcher.group(2));
                        result += a * b;
                    }
                }
            }
        }
        return result;
    }

}
