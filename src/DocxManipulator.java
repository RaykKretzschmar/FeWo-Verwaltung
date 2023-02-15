import java.io.*;
import java.net.URI;
import java.util.*;
import java.util.zip.*;

import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.servlet.http.HttpServletResponse;

import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.apache.poi.xwpf.usermodel.*;
import org.apache.poi.openxml4j.opc.*;

public class DocxManipulator {

  private static final String MAIN_DOCUMENT_PATH = "word/document.xml";
  private static final String TEMPLATE_DIRECTORY_ROOT = "TEMPLATES_DIRECTORY/";

  /* PUBLIC METHODS */

  /**
   * Generates .docx document from given template and the substitution data
   * 
   * @param templateName
   *                         Template data
   * @param substitutionData
   *                         Hash map with the set of key-value pairs that
   *                         represent substitution data
   * @return
   */
  public static Boolean generateAndSendDocx(String templateName, Map<String, String> substitutionData) {

    String templateLocation = TEMPLATE_DIRECTORY_ROOT + templateName;

    String userTempDir = UUID.randomUUID().toString();
    userTempDir = TEMPLATE_DIRECTORY_ROOT + userTempDir + "/";

    try {

      // Unzip .docx file
      unzip(new File(templateLocation), new File(userTempDir));

      // Change data
      changeData(new File(userTempDir + MAIN_DOCUMENT_PATH), substitutionData);

      // Rezip .docx file
      zip(new File(userTempDir), new File(userTempDir + templateName));

      // Send HTTP response
      sendDOCXResponse(new File(userTempDir + templateName), templateName);

      // Clean temp data
      deleteTempData(new File(userTempDir));
    } catch (IOException ioe) {
      System.out.println(ioe.getMessage());
      return false;
    }

    return true;
  }

  /* PRIVATE METHODS */

  /**
   * Unzipps specified ZIP file to specified directory
   * 
   * @param zipfile
   *                  Source ZIP file
   * @param directory
   *                  Destination directory
   * @throws IOException
   */
  private static void unzip(File zipfile, File directory) throws IOException {

    ZipFile zfile = new ZipFile(zipfile);
    Enumeration<? extends ZipEntry> entries = zfile.entries();

    while (entries.hasMoreElements()) {
      ZipEntry entry = entries.nextElement();
      File file = new File(directory, entry.getName());
      if (entry.isDirectory()) {
        file.mkdirs();
      } else {
        file.getParentFile().mkdirs();
        InputStream in = zfile.getInputStream(entry);
        try {
          copy(in, file);
        } finally {
          in.close();
        }
      }
    }
  }

  /**
   * Substitutes keys found in target file with corresponding data
   * 
   * @param targetFile
   *                         Target file
   * @param substitutionData
   *                         Map of key-value pairs of data
   * @throws IOException
   */
  @SuppressWarnings({ "unchecked", "rawtypes" })
  private static void changeData(File targetFile, Map<String, String> substitutionData) throws IOException {

    BufferedReader br = null;
    String docxTemplate = "";
    try {
      br = new BufferedReader(new InputStreamReader(new FileInputStream(targetFile), "UTF-8"));
      String temp;
      while ((temp = br.readLine()) != null){
        docxTemplate = docxTemplate + temp;
      }
      br.close();
      targetFile.delete();
    } catch (IOException e) {
      br.close();
      throw e;
    }

    Iterator substitutionDataIterator = substitutionData.entrySet().iterator();
    while (substitutionDataIterator.hasNext()) {
      Map.Entry<String, String> pair = (Map.Entry<String, String>) substitutionDataIterator.next();
      if (docxTemplate.contains(pair.getKey())) {
        if (pair.getValue() != null)
          docxTemplate = docxTemplate.replace(pair.getKey(), pair.getValue());
        else
          docxTemplate = docxTemplate.replace(pair.getKey(), "NEDOSTAJE");
      }
    }

    FileOutputStream fos = null;
    try {
      fos = new FileOutputStream(targetFile);
      fos.write(docxTemplate.getBytes("UTF-8"));
      fos.close();
    } catch (IOException e) {
      fos.close();
      throw e;
    }
  }

  /**
   * Zipps specified directory and all its subdirectories
   * 
   * @param directory
   *                  Specified directory
   * @param zipfile
   *                  Output ZIP file name
   * @throws IOException
   */
  private static void zip(File directory, File zipfile) throws IOException {

    URI base = directory.toURI();
    Deque<File> queue = new LinkedList<File>();
    queue.push(directory);
    OutputStream out = new FileOutputStream(zipfile);
    Closeable res = out;

    try {
      ZipOutputStream zout = new ZipOutputStream(out);
      res = zout;
      while (!queue.isEmpty()) {
        directory = queue.pop();
        for (File kid : directory.listFiles()) {
          String name = base.relativize(kid.toURI()).getPath();
          if (kid.isDirectory()) {
            queue.push(kid);
            name = name.endsWith("/") ? name : name + "/";
            zout.putNextEntry(new ZipEntry(name));
          } else {
            if (kid.getName().contains(".docx"))
              continue;
            zout.putNextEntry(new ZipEntry(name));
            copy(kid, zout);
            zout.closeEntry();
          }
        }
      }
    } finally {
      res.close();
    }
  }

  /**
   * Sends HTTP Response containing .docx file to Client
   * 
   * @param generatedFile
   *                      Path to generated .docx file
   * @param fileName
   *                      File name of generated file that is being presented to
   *                      user
   * @throws IOException
   */
  private static void sendDOCXResponse(File generatedFile, String fileName) throws IOException {

    FacesContext facesContext = FacesContext.getCurrentInstance();
    ExternalContext externalContext = facesContext.getExternalContext();
    HttpServletResponse response = (HttpServletResponse) externalContext
        .getResponse();

    BufferedInputStream input = null;
    BufferedOutputStream output = null;

    response.reset();
    response.setHeader("Content-Type", "application/msword");
    response.setHeader("Content-Disposition", "attachment; filename=\"" + fileName + "\"");
    response.setHeader("Content-Length", String.valueOf(generatedFile.length()));

    input = new BufferedInputStream(new FileInputStream(generatedFile), 10240);
    output = new BufferedOutputStream(response.getOutputStream(), 10240);

    byte[] buffer = new byte[10240];
    for (int length; (length = input.read(buffer)) > 0;) {
      output.write(buffer, 0, length);
    }

    output.flush();
    input.close();
    output.close();

    // Inform JSF not to proceed with rest of life cycle
    facesContext.responseComplete();
  }

  /**
   * Deletes directory and all its subdirectories
   * 
   * @param file
   *             Specified directory
   * @throws IOException
   */
  public static void deleteTempData(File file) throws IOException {

    if (file.isDirectory()) {

      // directory is empty, then delete it
      if (file.list().length == 0)
        file.delete();
      else {
        // list all the directory contents
        String files[] = file.list();

        for (String temp : files) {
          // construct the file structure
          File fileDelete = new File(file, temp);
          // recursive delete
          deleteTempData(fileDelete);
        }

        // check the directory again, if empty then delete it
        if (file.list().length == 0)
          file.delete();
      }
    } else {
      // if file, then delete it
      file.delete();
    }
  }

  private static void copy(InputStream in, OutputStream out) throws IOException {

    byte[] buffer = new byte[1024];
    while (true) {
      int readCount = in.read(buffer);
      if (readCount < 0) {
        break;
      }
      out.write(buffer, 0, readCount);
    }
  }

  private static void copy(File file, OutputStream out) throws IOException {
    InputStream in = new FileInputStream(file);
    try {
      copy(in, out);
    } finally {
      in.close();
    }
  }

  private static void copy(InputStream in, File file) throws IOException {
    OutputStream out = new FileOutputStream(file);
    try {
      copy(in, out);
    } finally {
      out.close();
    }
  }

  public static void replaceIn(String inputFileName, String key, String replacement, String outputFileName) throws IOException, 
    InvalidFormatException, org.apache.poi.openxml4j.exceptions.InvalidFormatException {
      try {

       /**
        * if uploaded doc then use HWPF else if uploaded Docx file use
        * XWPFDocument
        */
       XWPFDocument doc = new XWPFDocument(
         //OPCPackage.open("d:\\1\\rpt.docx"));
         OPCPackage.open(inputFileName));
       for (XWPFParagraph p : doc.getParagraphs()) {
        List<XWPFRun> runs = p.getRuns();
        if (runs != null) {
         for (XWPFRun r : runs) {
          String text = r.getText(0);
          if (text != null && text.contains(key)) {
           text = text.replace(key, replacement);//your content
           r.setText(text, 0);
          }
         }
        }
       }

       for (XWPFTable tbl : doc.getTables()) {
        for (XWPFTableRow row : tbl.getRows()) {
         for (XWPFTableCell cell : row.getTableCells()) {
          for (XWPFParagraph p : cell.getParagraphs()) {
           for (XWPFRun r : p.getRuns()) {
            String text = r.getText(0);
            if (text != null && text.contains(key)) {
             text = text.replace(key, replacement);
             r.setText(text, 0);
            }
           }
          }
         }
        }
       }

       //doc.write(new FileOutputStream("d:\\1\\output.docx"));
       doc.write(new FileOutputStream(outputFileName));
      } finally {

      }
    }
}