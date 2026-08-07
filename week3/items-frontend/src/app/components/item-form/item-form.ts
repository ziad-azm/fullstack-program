import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { ItemService } from '../../services/item.service';

@Component({
  selector: 'app-item-form',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './item-form.html',
  styleUrl: './item-form.css',
})
export class ItemForm {
  private readonly fb = inject(FormBuilder);
  private readonly itemService = inject(ItemService);
  private readonly router = inject(Router);

  protected readonly submitting = signal(false);
  protected readonly error = signal<string | null>(null);

  protected readonly form = this.fb.group({
    name: ['', [Validators.required]],
    price: [null as number | null, [Validators.required, Validators.min(0.01)]],
    in_stock: [true],
  });

  get name() {
    return this.form.controls.name;
  }

  get price() {
    return this.form.controls.price;
  }

  onSubmit(): void {
    if (this.form.invalid || this.submitting()) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitting.set(true);
    this.error.set(null);

    const { name, price, in_stock } = this.form.getRawValue();

    this.itemService.createItem({ name: name!, price: price!, in_stock: in_stock! }).subscribe({
      next: () => {
        this.submitting.set(false);
        this.form.reset({ name: '', price: null, in_stock: true });
        this.router.navigate(['/']);
      },
      error: () => {
        this.submitting.set(false);
        this.error.set('Failed to create item. Please try again.');
      },
    });
  }
}
