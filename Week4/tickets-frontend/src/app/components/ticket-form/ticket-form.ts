import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, output, signal } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  ReactiveFormsModule,
  ValidationErrors,
  Validators,
} from '@angular/forms';

import { TICKET_PRIORITIES, TicketPriority } from '../../models/ticket.model';
import { TicketService } from '../../services/ticket.service';

/** The API rejects whitespace-only titles, so reuse the `required` key for them. */
function nonBlank(control: AbstractControl): ValidationErrors | null {
  return typeof control.value === 'string' && control.value.trim().length === 0
    ? { required: true }
    : null;
}

@Component({
  selector: 'app-ticket-form',
  imports: [ReactiveFormsModule],
  templateUrl: './ticket-form.html',
  styleUrl: './ticket-form.css',
})
export class TicketForm {
  /** Emitted after a successful create so the list can refresh. */
  readonly created = output<void>();

  private readonly fb = inject(FormBuilder);
  private readonly ticketService = inject(TicketService);

  protected readonly submitting = signal(false);
  protected readonly error = signal<string | null>(null);

  protected readonly priorities = TICKET_PRIORITIES;

  protected readonly form = this.fb.group({
    title: ['', [Validators.required, nonBlank, Validators.maxLength(150)]],
    description: ['', [Validators.maxLength(2000)]],
    priority: ['medium' as TicketPriority, [Validators.required]],
  });

  protected get title() {
    return this.form.controls.title;
  }

  protected get description() {
    return this.form.controls.description;
  }

  onSubmit(): void {
    if (this.form.invalid || this.submitting()) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitting.set(true);
    this.error.set(null);

    const { title, description, priority } = this.form.getRawValue();

    this.ticketService
      .createTicket({
        title: title!.trim(),
        description: description?.trim() || undefined,
        priority: priority!,
      })
      .subscribe({
        next: () => {
          this.submitting.set(false);
          this.form.reset({ title: '', description: '', priority: 'medium' });
          this.created.emit();
        },
        error: (err: HttpErrorResponse) => {
          this.submitting.set(false);
          this.error.set(this.messageFor(err));
        },
      });
  }

  /** Surfaces the API's `{ detail: [{ field, message }] }` validation errors. */
  private messageFor(err: HttpErrorResponse): string {
    const detail = err.error?.detail;

    if (Array.isArray(detail)) {
      return detail.map((item) => item.message).join(', ');
    }
    if (typeof detail === 'string') {
      return detail;
    }
    return 'Failed to create the ticket. Please try again.';
  }
}
