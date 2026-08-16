import { Routes } from '@angular/router';

import { TicketList } from './components/ticket-list/ticket-list';

export const routes: Routes = [
  // The list screen hosts the create form, so the whole feature lives on one route.
  { path: '', component: TicketList },
  { path: '**', redirectTo: '' },
];
