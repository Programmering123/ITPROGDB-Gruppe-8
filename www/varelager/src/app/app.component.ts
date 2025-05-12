import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core'; // Importer ViewChild og AfterViewInit
import { HttpClient } from '@angular/common/http';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common'; // Importer CommonModule for ngIf og ngFor

// Material Moduler
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator'; // Importer MatPaginator
import { MatSort, MatSortModule } from '@angular/material/sort'; // Importer MatSort og MatSortModule
import { MatTableDataSource, MatTableModule } from '@angular/material/table'; // Importer MatTableDataSource

// Definer en interface for vare-objektene for bedre typesikkerhet
export interface Vare {
  VNr: string;
  Betegnelse: string;
  Pris: number;
  Antall: number;
  // Legg til andre felt hvis API-et returnerer flere som du vil bruke
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    MatPaginatorModule,
    MatTableModule,
    MatSortModule // Legg til MatSortModule her
],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterViewInit { // Implementer AfterViewInit
  // Bruk MatTableDataSource for å få innebygd funksjonalitet for sortering og paginering
  dataKilde: MatTableDataSource<Vare>;
  isLoading = true;

  displayedColumns: string[] = ['VNr', 'Betegnelse', 'Pris', 'Antall'];

  // Bruk ViewChild for å få tak i referanser til paginator og sort i template-en
  // Bruker '!' for "definite assignment assertion" siden de vil bli initialisert i ngAfterViewInit
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private http: HttpClient) {
    // Initialiser MatTableDataSource her eller i ngOnInit
    this.dataKilde = new MatTableDataSource<Vare>([]);
    this.fetchData(); // Hent data i konstruktøren eller i ngOnInit
  }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.isLoading = true;
    // Sørg for at dette er korrekt API endepunkt
    this.http.get<Vare[]>('http://localhost:5000/api/varer')
      .subscribe({
        next: (data) => {
          this.dataKilde = new MatTableDataSource(data); // Sett data på MatTableDataSource
          this.isLoading = false;
          console.log('Data mottatt:', data);
          // Koble paginator og sort etter at data er lastet og ViewChildren er initialisert (via ngAfterViewInit)
          // Hvis du vil være ekstra sikker, kan du re-tildele dem her også, men ngAfterViewInit er vanligvis nok.
          this.dataKilde.paginator = this.paginator;
          this.dataKilde.sort = this.sort;
        },
        error: (error) => {
          console.error('Feil med henting av data:', error);
          this.dataKilde.data = []; // Tøm data ved feil
          this.isLoading = false;
        }
      });
  }

  ngAfterViewInit(): void {
    // Koble paginator og sort til datakilden etter at viewet er initialisert
    // Dette sikrer at @ViewChild referansene (paginator og sort) er tilgjengelige.
    this.dataKilde.paginator = this.paginator;
    this.dataKilde.sort = this.sort;
  }
}