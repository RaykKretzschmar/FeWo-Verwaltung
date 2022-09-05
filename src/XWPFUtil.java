import java.io.*;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;

public final class XWPFUtil {

    public static boolean remove(XWPFParagraph paragraph, XWPFDocument doc) {
        doc.removeBodyElement(doc.getPosOfParagraph(paragraph));
        return true;
    }

    public static XWPFParagraph insertAfter(XWPFParagraph paragraph, XWPFDocument doc) {
        XWPFParagraph next = next(paragraph, doc);
        XmlCursor cursor = next.getCTP().newCursor();
        return doc.insertNewParagraph(cursor);
    }

    public static XWPFParagraph insertBefore(XWPFParagraph paragraph, XWPFDocument doc) {
        XmlCursor cursor = paragraph.getCTP().newCursor();
        return doc.insertNewParagraph(cursor);
    }

    public static XWPFParagraph next(XWPFParagraph paragraph, XWPFDocument doc) {
        int position = doc.getPosOfParagraph(paragraph);
        return doc.getParagraphs().get(++position);
    }

    public static XWPFParagraph find(String text, XWPFDocument doc) {
        for (XWPFParagraph p : doc.getParagraphs()) {
            if (p.getText().contains(text))
                return p;
        }
        return null;
    }

    public static boolean hasPersonMark(XWPFDocument doc) {
        for (String mark : getMarks(doc))
            if (mark.contains("Person"))
                return true;
        return false;
    }

    public static Set<String> getMarks(XWPFDocument doc) {
        StringBuilder text = new StringBuilder();
        for (XWPFParagraph paragraph : doc.getParagraphs())
            collectAllCharacters(text, paragraph.getRuns());
        Set<String> marks = new HashSet<>();
        marks.addAll(StringUtil.getAllSubstrings(text.toString(), "#{", "}"));
        marks.addAll(getHeaderMarks(doc));
        marks.addAll(getFooterMarks(doc));
        marks.addAll(getTableMarks(doc));
        return marks;
    }

    private static Set<String> getHeaderMarks(XWPFDocument doc) {
        StringBuilder text = new StringBuilder();
        for (XWPFHeader header : doc.getHeaderList())
            for (XWPFParagraph paragraph : header.getListParagraph())
                collectAllCharacters(text, paragraph.getRuns());
        return new HashSet<>(StringUtil.getAllSubstrings(text.toString(), "#{", "}"));
    }

    private static Set<String> getFooterMarks(XWPFDocument doc) {
        StringBuilder text = new StringBuilder();
        for (XWPFFooter footer : doc.getFooterList())
            for (XWPFParagraph paragraph : footer.getListParagraph())
                collectAllCharacters(text, paragraph.getRuns());
        return new HashSet<>(StringUtil.getAllSubstrings(text.toString(), "#{", "}"));
    }

    private static Set<String> getTableMarks(XWPFDocument doc) {
        StringBuilder text = new StringBuilder();
        for (XWPFTable xwpfTable : doc.getTables()) {
            List<XWPFTableRow> tableRows = xwpfTable.getRows();
            for (XWPFTableRow xwpfTableRow : tableRows) {
                List<XWPFTableCell> tableCells = xwpfTableRow.getTableCells();
                for (XWPFTableCell xwpfTableCell : tableCells) {
                    for (XWPFParagraph paragraph : xwpfTableCell.getParagraphs())
                        collectAllCharacters(text, paragraph.getRuns());
                }
            }
        }
        return new HashSet<>(StringUtil.getAllSubstrings(text.toString(), "#{", "}"));
    }

    private static void collectAllCharacters(StringBuilder text, List<XWPFRun> runs) {
        if (runs != null) {
            for (XWPFRun r : runs) {
                int pos = r.getTextPosition();
                pos = -1;
                // TODO:
                if (r.getText(pos) != null)
                    text.append(r.getText(pos));
            }
        }
    }

    public static void replaceMark(XWPFDocument doc, ObjectMap replacements) {
        Map<String, String> map = new HashMap<>();
        for (Map.Entry<String, Object> entry : replacements.entrySet())
            map.put(entry.getKey(), String.valueOf(entry.getValue()));
        replaceMark(doc, map);
    }

    public static void replaceMark(XWPFDocument doc, Map<String, String> replacements) {
        replaceInParagraphs(doc.getParagraphs(), replacements);
        replaceInTables(doc, replacements);
        replaceInHeader(doc, replacements);
        replaceInFooter(doc, replacements);
    }

    public static void replaceInTables(XWPFDocument doc, Map<String, String> replacements) {
        for (XWPFTable xwpfTable : doc.getTables()) {
            List<XWPFTableRow> tableRows = xwpfTable.getRows();
            for (XWPFTableRow xwpfTableRow : tableRows) {
                List<XWPFTableCell> tableCells = xwpfTableRow.getTableCells();
                for (XWPFTableCell xwpfTableCell : tableCells) {
                    replaceInParagraphs(xwpfTableCell.getParagraphs(), replacements);
                }
            }
        }
    }

    public static void replaceInHeader(XWPFDocument doc, Map<String, String> replacements) {
        for (XWPFHeader header : doc.getHeaderList())
            replaceInParagraphs(header.getParagraphs(), replacements);
    }

    public static void replaceInFooter(XWPFDocument doc, Map<String, String> replacements) {
        for (XWPFFooter footer : doc.getFooterList())
            replaceInParagraphs(footer.getParagraphs(), replacements);
    }

    public static void replaceInParagraphs(List<XWPFParagraph> paragraphs, Map<String, String> replacements) {
        replaceInParagraphs(paragraphs, replacements, '#', '{', '}');
    }

    public static void replaceInParagraphs(List<XWPFParagraph> paragraphs, Map<String, String> replacements,
            Character startCharacter, Character secondStartCharacter, Character endCharacter) {
        mergeTextForVariables(paragraphs, startCharacter, secondStartCharacter, endCharacter);
        for (XWPFParagraph paragraph : paragraphs) {
            for (XWPFRun run : paragraph.getRuns()) {
                String text = run.getText(-1);
                if (text == null || text.equals(""))
                    continue;
                for (Map.Entry<String, String> replacement : replacements.entrySet()) {
                    String searchText = startCharacter.toString() + secondStartCharacter.toString()
                            + replacement.getKey() + endCharacter.toString();
                    text = text.replace(searchText, replacement.getValue());
                }
                run.setText(text, 0);
            }
        }
    }

    private static void mergeTextForVariables(List<XWPFParagraph> paragraphs, Character startCharacter,
            Character secondStartCharacter, Character endCharacter) {
        for (List<XWPFRun> list : collectSeparatedRuns(paragraphs, startCharacter, secondStartCharacter,
                endCharacter)) {
            XWPFRun firstRun = list.get(0);
            XWPFRun lastRun = list.get(list.size() - 1);
            for (XWPFRun run : list) {
                if (run == firstRun || run == lastRun)
                    continue;
                firstRun.setText(firstRun.getText(-1) + run.getText(-1), 0);
                run.setText("", 0);
            }
            String lastRunText = lastRun.getText(-1);
            firstRun.setText(firstRun.getText(-1) + lastRunText.substring(0, lastRunText.indexOf(endCharacter) + 1), 0);
            lastRun.setText(lastRunText.substring(lastRunText.indexOf(endCharacter) + 1), 0);
        }
    }

    private static List<List<XWPFRun>> collectSeparatedRuns(List<XWPFParagraph> paragraphs, Character startCharacter,
            Character secondStartCharacter, Character endCharacter) {
        List<List<XWPFRun>> collection = new ArrayList<>();
        List<XWPFRun> tempList = new ArrayList<>();
        DetectionType currentType = DetectionType.NONE;
        for (XWPFParagraph paragraph : paragraphs) {
            Character lastCharacter = null;
            for (XWPFRun run : paragraph.getRuns()) {
                String text = run.getText(-1);
                DetectionType type = detectRun(run, currentType, lastCharacter, startCharacter, secondStartCharacter,
                        endCharacter);
                if (text != null) {
                    if (text.length() > 1)
                        lastCharacter = text.charAt(text.length() - 1);
                    else if (text.length() == 1)
                        lastCharacter = text.charAt(0);
                }
                if (currentType == DetectionType.NONE && type == DetectionType.CONTINUE) {
                    tempList.add(run);
                } else if (currentType == DetectionType.CONTINUE && type == DetectionType.CONTINUE) {
                    tempList.add(run);
                } else if (currentType == DetectionType.CONTINUE && type == DetectionType.NONE) {
                    tempList.clear();
                } else if (currentType == DetectionType.CONTINUE && type == DetectionType.END) {
                    tempList.add(run);
                    List<XWPFRun> l = new ArrayList<>();
                    l.addAll(tempList);
                    collection.add(l);
                    tempList.clear();
                    lastCharacter = null;
                }
                currentType = type;
            }
        }
        return collection;
    }

    private static DetectionType detectRun(XWPFRun run, DetectionType type, Character lastCharacter,
            Character startCharacter, Character secondStartCharacter, Character endCharacter) {
        String text = run.getText(-1);
        if (text == null)
            return DetectionType.NONE;
        if (type == DetectionType.NONE) {
            if (!text.contains(startCharacter.toString()))
                return DetectionType.NONE;
            if (isOpen(text, false, null, startCharacter, secondStartCharacter, endCharacter))
                return DetectionType.CONTINUE;
            return DetectionType.END;
        } else if (type == DetectionType.CONTINUE) {
            if (isOpen(text, true, lastCharacter, startCharacter, secondStartCharacter, endCharacter))
                return DetectionType.CONTINUE;
            if (lastCharacter == startCharacter)
                return DetectionType.NONE;
            return DetectionType.END;
        }
        return DetectionType.NONE;
    }

    private static boolean isOpen(String text, boolean state, Character lastCharacter, Character startCharacter,
            Character secondStartCharacter, Character endCharacter) {
        boolean open = state;
        Character last = lastCharacter;
        for (char c : text.toCharArray()) {
            if (last == null)
                last = c;
            if (open) {
                if (last == startCharacter && c != secondStartCharacter)
                    open = false;
                else if (c == endCharacter)
                    open = false;
            } else {
                if (c == startCharacter)
                    open = true;
            }
            last = c;
        }
        return open;
    }

    private enum DetectionType {
        NONE, CONTINUE, END;
    }

}