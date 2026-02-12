import { Routes } from '@angular/router';
import {Pi1} from './main-page/pi1/pi1';
import {Pi2} from './main-page/pi2/pi2';
import {Pi3} from './main-page/pi3/pi3';
import {Home} from './main-page/home/home';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: Home },
  { path: 'pi1', component: Pi1 },
  { path: 'pi2', component: Pi2 },
  { path: 'pi3', component: Pi3 },
];
