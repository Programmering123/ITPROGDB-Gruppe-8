import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';    // Importer ViewChild og AfterViewInit
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';                                 // Importer CommonModule for ngIf og ngFor

// Material Moduler
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator'; // Importer MatPaginator
import { MatSort, MatSortModule } from '@angular/material/sort';                // Importer MatSort og MatSortModule
import { MatTableDataSource, MatTableModule } from '@angular/material/table';   // Importer MatTableDataSource

// Definerer en interface for vare-objektene for bedre typesikkerhet:
export interface Vare {
  VNr: string;
  Betegnelse: string;
  Pris: number;
  Antall: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    MatPaginatorModule,
    MatTableModule,
    MatSortModule 
],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterViewInit { 
  dataKilde: MatTableDataSource<Vare>;
  isLoading = true;

  displayedColumns: string[] = ['VNr', 'Betegnelse', 'Pris', 'Antall'];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private http: HttpClient) {
    this.dataKilde = new MatTableDataSource<Vare>([]);
    this.fetchData(); 
  }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.isLoading = true;
    this.http.get<Vare[]>('http://localhost:5000/api/varer')
      .subscribe({
        next: (data) => {
          this.dataKilde = new MatTableDataSource(data); 
          this.isLoading = false;
          this.dataKilde.paginator = this.paginator;
          this.dataKilde.sort = this.sort;
        },
        error: (error) => {
          console.error('Feil med henting av data:', error);
          this.dataKilde.data = [];                                             // Tøm dataKilde ved feil 
          this.isLoading = false;
        }
      });
  }

  ngAfterViewInit(): void {
    this.dataKilde.paginator = this.paginator;
    this.dataKilde.sort = this.sort;
  }
}