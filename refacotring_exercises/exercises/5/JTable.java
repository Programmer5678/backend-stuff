import javax.accessibility.Accessible;
import javax.swing.JComponent;
import javax.swing.Scrollable;
import javax.swing.event.CellEditorListener;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.TableColumnModelListener;
import javax.swing.event.TableModelListener;

import javax.swing.table.TableModel;
import javax.swing.table.TableColumnModel;
import javax.swing.table.TableColumn;
import javax.swing.table.TableCellEditor;
import javax.swing.table.TableCellRenderer;
import javax.swing.table.JTableHeader;
import javax.swing.table.TableUI;

import javax.swing.event.TableColumnModelEvent;
import javax.swing.event.TableModelEvent;

import java.awt.*;
import java.util.List;
import java.util.Iterator;
import java.util.EventObject;
import java.awt.event.MouseEvent;

public class JTable extends JComponent implements
        Accessible,
        CellEditorListener,
        ListSelectionListener,
        Scrollable,
        TableColumnModelListener,
        TableModelListener {

    // Constants
    public static final int AUTO_RESIZE_ALL_COLUMNS = 0;
    public static final int AUTO_RESIZE_LAST_COLUMN = 1;
    public static final int AUTO_RESIZE_NEXT_COLUMN = 2;
    public static final int AUTO_RESIZE_OFF = 3;
    public static final int AUTO_RESIZE_SUBSEQUENT_COLUMNS = 4;

    // Constructors - filling the table
    public JTable() { }

    public JTable(TableModel model, TableColumnModel columnModel) { }

    public JTable(TableModel model, TableColumnModel columnModel,
                 ListSelectionModel selectionModel) { }

    public JTable(int rowCount, int columnCount) { }

    public JTable(Object[][] rowData, Object[][] columnNames) { }

    public JTable(java.util.Vector rowData, java.util.Vector columnNames) { }







        // add start-finish for selection
    public void addColumnSelectionInterval(int start, int finish) { }

    // add start-finsih for selection - rows
    public void addRowSelectionInterval(int start, int finish) { }

    //clear selection
    public void clearSelection() { }

    //
    public void columnSelectionChanged(ListSelectionEvent event) { }

    public boolean getCellSelectionEnabled() { return false; }

    public Boolean getColumnSelectionAllowed() { return null; }

    public Boolean getRowSelectionAllowed() { return null; }

    public void setRowSelectionAllowed(Boolean maySelect) { }

    public void setSelectionBackground(Color background) { }

    public void setSelectionForeground(Color foreground) { }

    public void setSelectionMode(int mode) { }

    public void setSelectionModel(ListSelectionModel model) { }

    public int getSelectedColumn() { return 0; }

    public int getSelectedColumnCount() { return 0; }

    public int[] getSelectedColumns() { return null; }

    public int getSelectedRow() { return 0; }

    public int getSelectedRowCount() { return 0; }

    public int[] getSelectedRows() { return null; }

    public Color getSelectionBackground() { return null; }

    public Color getSelectionForeground() { return null; }

    public ListSelectionModel getSelectionModel() { return null; }

    public Boolean isCellSelected(int row, int column) { return null; }

    public Boolean isColumnSelected(int column) { return null; }

        public Boolean isRowSelected(int row) { return null; }









    // Methods
    public void addColumn(TableColumn column) { }

    

    public void addNotify() { }

    

    public void columnAdded(TableColumnModelEvent event) { }

    public void columnAtPoint(Point p) { }

    public void columnMarginChanged(ChangeEvent event) { }

    public void columnMoved(TableColumnModelEvent event) { }

    public void columnRemoved(TableColumnModelEvent event) { }

    

    public void convertColumnIndexToModel(int viewColumn) { }

    public void convertColumnIndexToView(int modelColumn) { }

    public void createDefaultColumnsFromModel() { }

    public boolean editCellAt(int row, int column) { return false; }

    public boolean editCellAt(int row, int column, EventObject event) { return false; }

    public void editingCanceled(ChangeEvent event) { }

    public void editingStopped(ChangeEvent event) { }

    public AccessibleContext getAccessibleContext() { return null; }

    public boolean getAutoCreateColumnsFromModel() { return false; }

    public int getAutoResizeMode() { return 0; }

    public TableCellEditor getCellEditor() { return null; }

    public TableCellEditor getCellEditor(int row, int column) { return null; }

    public Rectangle getCellRect(int row, int column, boolean includeSpacing) { return null; }



    public TableColumn getColumn(Object object) { return null; }

    public Class getColumnClass(int column) { return null; }

    public int getColumnCount() { return 0; }

    public TableColumnModel getColumnModel() { return null; }

    public String getColumnName(int column) { return null; }


    public TableCellEditor getDefaultEditor(Class clazz) { return null; }

    public TableCellRenderer getDefaultRenderer(Class clazz) { return null; }

    public int getEditingColumn() { return 0; }

    public int getEditingRow() { return 0; }

    public Component getEditorComponent() { return null; }

    public Color getGridColor() { return null; }

    public Dimension getIntercellSpacing() { return null; }

    public TableModel getModel() { return null; }

    public Dimension getPreferredScrollableViewportSize() { return null; }

    public int getRowCount() { return 0; }

    public int getRowHeight() { return 0; }

    public int getRowMargin() { return 0; }


    public int getScrollableBlockIncrement(Rectangle visible, int orientation, int direction) { return 0; }

    public Boolean getScrollableTracksViewportHeight() { return null; }

    public Boolean getScrollableTracksViewportWidth() { return null; }

    public int getScrollableUnitIncrement(Rectangle visible, int orientation, int direction) { return 0; }



    public Boolean getShowHorizontalLines() { return null; }

    public Boolean getShowVerticalLines() { return null; }

    public JTableHeader getTableHeader() { return null; }

    public String getToolTipText(MouseEvent event) { return null; }

    public TableUI getUI() { return null; }

    public String getUIClassID() { return null; }

    public Object getValueAt(int row, int column) { return null; }

    public Boolean isCellEditable(int row, int column) { return null; }


    public Boolean isEditing() { return null; }

    public boolean isManagingFocus() { return false; }


    public void moveColumn(int column, int newColumn) { }

    public Component prepareEditor(TableCellEditor editor, int row, int column) { return null; }

    public Component prepareRenderer(TableCellRenderer renderer, int row, int column) { return null; }

    public void removeColumn(TableColumn column) { }

    public void removeColumnSelectionInterval(int column1, int column2) { }

    public void removeEditor() { }

    public void removeRowSelectionInterval(int row1, int row2) { }

    public void reshape(int x, int y, int width, int height) { }

    public int rowAtPoint(Point point) { return 0; }

    public void selectAll() { }

    public void setAutoCreateColumnsFromModel(Boolean doAutoCreate) { }

    public void setAutoResizeModel(int mode) { }

    public void setCellEditor(TableCellEditor editor) { }


    public void setColumnModel(TableColumnModel model) { }

    public void setColumnSelectionAllowed(Boolean maySelect) { }

    public void setColumnSelectionInterval(int column1, int column2) { }

    public void setDefaultEditor(Class clazz, TableCellEditor editor) { }

    public void setDefaultRenderer(Class clazz, TableCellRenderer renderer) { }

    public void setEditingColumn(int column) { }

    public void setEditingRow(int row) { }

    public void setGridColor(Color color) { }

    public void setIntercellSpacing(Dimension dim) { }

    public void setModel(TableModel model) { }

    public void setPreferredScrollableViewportSize(Dimension dim) { }

    public void setRowHeight(int height) { }

    public void setRowMargin(int margin) { }



    public void setShowGrid(Boolean showing) { }

    public void setShowHorizontalLines(Boolean b) { }

    public void setShowVerticalLines(Boolean b) { }

    public void setTableHeader(JTableHeader header) { }

    public void setUI(TableUI ui) { }

    public void setValueAt(Object value, int row, int column) { }

    public void sizeColumnsToFit(int resizingColumn) { }

    public void tableChanged(TableModelEvent event) { }

    public void updateUI() { }

    public void valueChanged(ListSelectionEvent event) { }
}
