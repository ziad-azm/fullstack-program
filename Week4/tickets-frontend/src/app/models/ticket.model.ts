export type TicketStatus = 'open' | 'in_progress' | 'closed';

export type TicketPriority = 'low' | 'medium' | 'high';

export interface Ticket {
  id: number;
  title: string;
  description: string | null;
  status: TicketStatus;
  priority: TicketPriority;
  created_at: string;
}

export interface TicketCreate {
  title: string;
  description?: string;
  status?: TicketStatus;
  priority?: TicketPriority;
}

export const TICKET_STATUSES: TicketStatus[] = ['open', 'in_progress', 'closed'];

export const TICKET_PRIORITIES: TicketPriority[] = ['low', 'medium', 'high'];

const STATUS_LABELS: Record<TicketStatus, string> = {
  open: 'Open',
  in_progress: 'In progress',
  closed: 'Closed',
};

export function statusLabel(status: TicketStatus): string {
  return STATUS_LABELS[status];
}
