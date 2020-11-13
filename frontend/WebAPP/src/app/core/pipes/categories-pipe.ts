import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'categoriesNames'})
export class CategoriesNamesPipe implements PipeTransform {
  transform(value): string {
    switch (value) {
        case 'produccion/operarios':
            return 'Producción - Operarios';
        
        case 'almacenamiento/logistica':
            return 'Almacenamiento - Logística';
        
        case 'ventas':
            return 'Ventas';
        
        case 'recursosHumanos':
            return 'Recursos humanos';
        
        case 'administracion/finanzas':
            return 'Administración - Finanzas';
        
        case 'medicina/salud':
            return 'Medicina - Salud';
        
        case 'marketing':
            return 'Marketing';
        
        case 'construccion/obras':
            return 'Construcción - Obras';
        
        case 'programacion/tecnologia':
            return 'Programación - Tecnología';
        
        case 'serviciosGenerales':
            return 'Servicios generales';
        
        case 'hosteleria/turismo':
            return 'Hostelería - Turismo';
        
        case 'ingenieria/arquitectura':
            return 'Ingeniería - Arquitectura';
        
        case 'diseño/multimedia':
            return 'Diseño - Multimedia';
        
        case 'investigacion/calidad':
            return 'Investigación - Calidad';
        
        case 'compras/comercioExterior':
            return 'Compras - Comercio exterior';
        
        case 'legal':
            return 'Legal';
        
        default:
            return 'Otros';
    }
  }
}