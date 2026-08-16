import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TicketForm } from './ticket-form';

const API = 'http://localhost:8000/tickets';

describe('TicketForm', () => {
  let fixture: ComponentFixture<TicketForm>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TicketForm],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();

    fixture = TestBed.createComponent(TicketForm);
    httpMock = TestBed.inject(HttpTestingController);
    await fixture.whenStable();
  });

  afterEach(() => {
    httpMock.verify();
  });

  function submitButton(): HTMLButtonElement {
    return fixture.nativeElement.querySelector('button[type="submit"]');
  }

  async function typeTitle(value: string) {
    const input: HTMLInputElement = fixture.nativeElement.querySelector('#title');
    input.value = value;
    input.dispatchEvent(new Event('input'));
    await fixture.whenStable();
  }

  it('disables submit until a title is entered', async () => {
    expect(submitButton().disabled).toBe(true);

    await typeTitle('Printer is jammed');

    expect(submitButton().disabled).toBe(false);
  });

  it('rejects a whitespace-only title', async () => {
    await typeTitle('   ');

    expect(submitButton().disabled).toBe(true);
  });

  it('posts the ticket, clears the form and emits created', async () => {
    let emitted = 0;
    fixture.componentInstance.created.subscribe(() => (emitted += 1));

    await typeTitle('  Printer is jammed  ');
    submitButton().click();
    await fixture.whenStable();

    const request = httpMock.expectOne(API);
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({ title: 'Printer is jammed', priority: 'medium' });

    request.flush({
      id: 1,
      title: 'Printer is jammed',
      description: null,
      status: 'open',
      priority: 'medium',
      created_at: '2026-01-01T10:00:00Z',
    });
    await fixture.whenStable();

    expect(emitted).toBe(1);
    const input: HTMLInputElement = fixture.nativeElement.querySelector('#title');
    expect(input.value).toBe('');
  });

  it("shows the API's validation message when the create fails", async () => {
    await typeTitle('Printer is jammed');
    submitButton().click();
    await fixture.whenStable();

    httpMock.expectOne(API).flush(
      { detail: [{ field: 'title', message: 'title must be at most 150 characters' }] },
      { status: 400, statusText: 'Bad Request' },
    );
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toContain('title must be at most 150 characters');
  });
});
