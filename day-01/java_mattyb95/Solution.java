import java.util.*;
import java.util.stream.IntStream;

class Solution {

    // Day 1: Historian Hysteria

    public static void main(String[] args) {
        List<Integer> leftList = new ArrayList<>();
        List<Integer> rightList = new ArrayList<>();
        try (Scanner scanner = new Scanner(System.in)) {
            while (scanner.hasNextInt()) {
                leftList.add(scanner.nextInt());
                rightList.add(scanner.nextInt());
            }
        }

        // Part 1
        Collections.sort(leftList);
        Collections.sort(rightList);
        int totalDistance = IntStream.range(0, leftList.size()).map(operand -> Math.abs(leftList.get(operand) - rightList.get(operand))).sum();
        System.out.println(totalDistance);

        //Part 2
        int similarityScore = 0;
        Map<Integer, Integer> similarityScoreMap = new HashMap<>();
        for (int value : leftList) {
            similarityScoreMap.putIfAbsent(value, value * Collections.frequency(rightList, value));
            similarityScore += similarityScoreMap.get(value);
        }
        System.out.println(similarityScore);
    }

}
