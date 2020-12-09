import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'imageReplacementCurriculumEdit'})
export class ImageReplacementCurriculumEdit implements PipeTransform {
  transform(value: string): string {
    if (value === 'data:image/png;base64,null' || value === null) {
        return 'https://w7.pngwing.com/pngs/340/956/png-transparent-profile-user-icon-computer-icons-user-profile-head-ico-miscellaneous-black-desktop-wallpaper.png';
    } else {
        return value;
    }
  }
}