from PyQt5 import QtWidgets, uic, QtSql, QtCore
from PyQt5.Qt import QDate
from PyQt5.QtSql import QSqlTableModel
import sys

class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('display.ui', self)
        self.dateEdit.setDate(QDate.currentDate())
        self.show()
        self.OpenDB()
        self.model = QtSql.QSqlTableModel()
        self.Display("")
        self.ex.hide()
        self.add.clicked.connect(self.Add)
        self.dlt.clicked.connect(self.Delete)
        self.pb_tggl.clicked.connect(self.Cari)

    def OpenDB(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('database.db')
        if not db.open():
            return False
        else:
            return True

    def Display(self,filterr):
        if filterr == "":
            self.model.setTable('Tabel')
        else:
            query = QtSql.QSqlQuery("select * from tabel ""where Tanggal like '%"+filterr + "%' ")
            self.model.setTable("")
            self.model.setQuery(query)
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Nama Penyewa")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Nomor Telepon")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Alamat")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Acara")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Waktu")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, "Tanggal")
        self.tableView.setModel(self.model)

    def Cari(self):
        cari = self.tggl.text()
        self.Display(cari)

    def Add(self):
        query = QtSql.QSqlQuery()
        waktu = ""
        if self.siang.isChecked():
            waktu = "Siang"
        if self.malam.isChecked():
            waktu = "Malam"

        date = self.dateEdit.date()
        nama = self.nama.text()
        notel = self.notel.text()
        alamat = self.alamat.text()
        acara = self.acara.text()
        
        if nama == '' or notel == '' or alamat == '' or acara == '' or self.ex.isChecked():
            self.Ok.setText('Data Tidak Boleh Kosong')
            self.Ok.setStyleSheet('background-color:red; color:white; border-radius:10px;')
        elif date <= QDate.currentDate():
            self.Ok.setText('Tanggal Sudah Berlalu. Booking Minimal Besok')
            self.Ok.setStyleSheet('background-color:red; color:white; border-radius:10px;')    
        else:
            if query.exec_("insert into Tabel values "
                    "('%s','%s','%s','%s','%s','%s')" %(nama,notel,alamat,acara,waktu,date.toString())):
                self.Display("")
                self.Ok.setText("Data Berhasil Ditambah")
                self.Ok.setStyleSheet('background-color:green; color:white; border-radius:10px;')
            else:
                self.Ok.setText('Jadwal Bentrok')
                self.Ok.setStyleSheet('background-color:red; color:white; border-radius:10px;')
        
            self.nama.clear()
            self.notel.clear()
            self.alamat.clear()
            self.acara.clear()
            self.ex.setCheckable(True)
            self.ex.setChecked(True)

    def Delete(self):
        self.model.removeRow(self.tableView.currentIndex().row())
        self.Display("")
        self.Ok.setText('Data Berhasil Dihapus')
        self.Ok.setStyleSheet('background-color:red; color:white; border-radius:10px;')
        self.nama.clear()
        self.notel.clear()
        self.alamat.clear()
        self.acara.clear()
        self.ex.setCheckable(True)
        self.ex.setChecked(True)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
