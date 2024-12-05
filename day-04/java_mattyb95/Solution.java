import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class Solution {

    private static final String WORD = "XMAS";
    private static final int[][] directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}};

    public static void main(String[] args) {
        List<List<Character>> grid = new ArrayList<>();
        try (Scanner scanner = new Scanner(System.in)) {
            while (scanner.hasNextLine()) grid.add(scanner.nextLine().chars().mapToObj(value -> (char) value).toList());
        }

        // Part 1
        System.out.println(countXmasOccurrences(grid));

        // Part 2
        System.out.println(countXmasPatterns(grid));
    }

    private static int countXmasOccurrences(List<List<Character>> grid) {
        int count = 0;
        for (int row = 0; row < grid.size(); row++)
            for (int col = 0; col < grid.get(row).size(); col++) count += searchFromCell(grid, row, col);
        return count;
    }

    private static int searchFromCell(List<List<Character>> grid, int row, int col) {
        return (int) Arrays.stream(directions).filter(direction -> searchWord(grid, row, col, direction)).count();
    }

    private static boolean searchWord(List<List<Character>> grid, int row, int col, int[] direction) {
        int gridSize = grid.size();
        int wordLength = WORD.length();
        int endRow = row + direction[0] * (wordLength - 1);
        int endCol = col + direction[1] * (wordLength - 1);
        if (endRow < 0 || endRow >= gridSize || endCol < 0 || endCol >= gridSize) return false;
        for (int i = 0; i < wordLength; i++) {
            int currentRow = row + i * direction[0];
            int currentCol = col + i * direction[1];
            if (grid.get(currentRow).get(currentCol) != WORD.charAt(i)) return false;
        }
        return true;
    }

    private static int countXmasPatterns(List<List<Character>> grid) {
        int count = 0;
        int[] dx = {-1, 1, -1, 1};
        int[] dy = {-1, 1, 1, -1};
        for (int i = 1; i < grid.size() - 1; i++) {
            for (int j = 1; j < grid.get(i).size() - 1; j++) {
                if (grid.get(i).get(j) == 'A') {
                    boolean isXMAS = true;
                    for (int direction = 0; direction < 4; direction += 2) {
                        char startChar = grid.get(i + dx[direction]).get(j + dy[direction]);
                        char endChar = grid.get(i + dx[direction + 1]).get(j + dy[direction + 1]);
                        if (!((startChar == 'M' && endChar == 'S') || (startChar == 'S' && endChar == 'M'))) {
                            isXMAS = false;
                            break;
                        }
                    }
                    if (isXMAS) count++;
                }
            }
        }
        return count;
    }

}
