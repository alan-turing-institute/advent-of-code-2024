import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Solution {

    // Day 2: Red-Nosed Reports

    private static final boolean PROBLEM_DAMPENER = true;

    public static void main(String[] args) {
        List<List<Integer>> reports = new ArrayList<>();
        try (Scanner scanner = new Scanner(System.in)) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                reports.add(Arrays.stream(line.split("\\s+")).map(Integer::parseInt).collect(Collectors.toList()));
            }
        }

        // Part 1
        System.out.println(reports.stream().filter(record -> isRecordSafe(record, !PROBLEM_DAMPENER)).count());

        // Part 2
        System.out.println(reports.stream().filter(record -> isRecordSafe(record, PROBLEM_DAMPENER)).count());
    }

    private static boolean isRecordSafe(List<Integer> record, boolean problemDampener) {
        boolean isRecordSafe = true;
        if (record.size() < 2) return true;
        if (problemDampener) {
            if (testBadIndex(record, 0)) return true;
            if (testBadIndex(record, record.size() - 1)) return true;
        }
        for (int index = 0; index < record.size() - 1; index++) {
            int currentValue = record.get(index);
            int nextValue = record.get(index + 1);
            if (!areAdjacent(currentValue, nextValue) || index > 0 && !isValidDirection(record, index)) {
                if (problemDampener) {
                    if (testBadIndex(record, index)) return true;
                    else isRecordSafe = false;
                } else return false;
            }
        }
        return isRecordSafe;
    }

    private static boolean testBadIndex(List<Integer> record, int index) {
        List<Integer> recordCopyOne = new ArrayList<>(record);
        recordCopyOne.remove(index);
        return isRecordSafe(recordCopyOne, !PROBLEM_DAMPENER);
    }

    private static boolean isValidDirection(List<Integer> record, int index) {
        int prevValue = record.get(index - 1);
        int currValue = record.get(index);
        int nextValue = record.get(index + 1);
        return prevValue <= currValue && currValue <= nextValue || prevValue >= currValue && currValue >= nextValue;
    }

    private static boolean areAdjacent(int a, int b) {
        int absoluteDifference = Math.abs(a - b);
        return absoluteDifference >= 1 && absoluteDifference <= 3;
    }

}
