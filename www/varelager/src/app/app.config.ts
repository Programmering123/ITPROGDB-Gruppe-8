import { ApplicationConfig, importProvidersFrom, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatTableModule } from '@angular/material/table';
import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';
import { APP_BASE_HREF, CommonModule, HashLocationStrategy, LocationStrategy } from '@angular/common';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    importProvidersFrom(MatPaginatorModule),
    provideHttpClient(),
    MatTableModule,
    { provide: APP_BASE_HREF, useValue: './' },
    { provide: 'BASE_URL', useValue: './' },
    { provide: 'API_URL', useValue: 'http://localhost:5000/' },
    { provide: LocationStrategy, useClass: HashLocationStrategy}, 
  ]
};
