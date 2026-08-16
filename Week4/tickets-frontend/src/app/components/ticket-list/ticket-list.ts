import { DatePipe } from '@angular/common';
import { Component, OnInit, signal } from '@angular/core';

import {
  TICKET_STATUSES,
  Ticket,
  TicketStatus,
  statusLabel,
} from '../../models/ticket.model';
import { TicketService } from '../../services/ticket.service';
import { TicketForm } from '../ticket-form/ticket-form';

type StatusFilter = TicketStatus | 'all';

@Component({
  selector: 'app-ticket-list',
  imports: [DatePipe, TicketForm],
  templateUrl: './ticket-list.html',
  styleUrl: './ticket-list.css',
})
export class TicketList implements OnInit {
  protected readonly tickets = signal<Ticket[]>([]);
  protected readonly loading = signal(false);
  protected readonly error = signal<string | null>(null);
  /** Errors from a status change / delete, kept separate from the load error. */
  protected readonly actionError = signal<string | null>(null);
  protected readonly filter = signal<StatusFilter>('all');
  /** Id of the ticket whose row action is in flight, so its buttons can disable. */
  protected readonly pendingId = signal<number | null>(null);

  protected readonly statuses = TICKET_STATUSES;
  protected readonly statusLabel = statusLabel;

  constructor(private readonly ticketService: TicketService) {}

  ngOnInit(): void {
    this.loadTickets();
  }

  loadTickets(): void {
    this.loading.set(true);
    this.error.set(null);

    const filter = this.filter();

    this.ticketService.getTickets(filter === 'all' ? undefined : filter).subscribe({
      next: (tickets) => {
        this.tickets.set(tickets);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Failed to load tickets. Is the API running at http://localhost:8000?');
        this.loading.set(false);
      },
    });
  }

  protected filterLabel(): string {
    const filter = this.filter();
    return filter === 'all' ? 'All' : statusLabel(filter);
  }

  onFilterChange(value: string): void {
    this.filter.set(value as StatusFilter);
    this.actionError.set(null);
    this.loadTickets();
  }

  onStatusChange(ticket: Ticket, value: string): void {
    const status = value as TicketStatus;
    if (status === ticket.status) {
      return;
    }

    this.pendingId.set(ticket.id);
    this.actionError.set(null);

    this.ticketService.updateStatus(ticket.id, status).subscribe({
      next: () => {
        this.pendingId.set(null);
        this.loadTickets();
      },
      error: () => {
        this.pendingId.set(null);
        this.actionError.set(`Failed to update ticket ${ticket.id}.`);
        // The dropdown already shows the status the user picked. Drop the rows so
        // the reload rebuilds them, snapping the select back to the API's state.
        this.tickets.set([]);
        this.loadTickets();
      },
    });
  }

  onDelete(ticket: Ticket): void {
    this.pendingId.set(ticket.id);
    this.actionError.set(null);

    this.ticketService.deleteTicket(ticket.id).subscribe({
      next: () => {
        this.pendingId.set(null);
        this.loadTickets();
      },
      error: () => {
        this.pendingId.set(null);
        this.actionError.set(`Failed to delete ticket ${ticket.id}.`);
      },
    });
  }
}
