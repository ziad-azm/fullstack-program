import { Routes } from '@angular/router';

import { ItemForm } from './components/item-form/item-form';
import { ItemList } from './components/item-list/item-list';

export const routes: Routes = [
  { path: '', component: ItemList },
  { path: 'new', component: ItemForm },
  { path: '**', redirectTo: '' },
];
