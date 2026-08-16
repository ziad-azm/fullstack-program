import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { Ticket } from '../../models/ticket.model';
import { TicketList } from './ticket-list';

const API = 'http://localhost:8000/tickets';

const TICKET: Ticket = {
  id: 1,
  title: 'Printer is jammed',
  description: '2nd floor',
  status: 'open',
  priority: 'high',
  created_at: '2026-01-01T10:00:00Z',
};

describe('TicketList', () => {
  let fixture: ComponentFixture<TicketList>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TicketList],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(TicketList);
    httpMock = TestBed.inject(HttpTestingController);
    await fixture.whenStable();
  });

  afterEach(() => {
    httpMock.verify();
  });

  /** Answers the GET the component issues and lets the view settle. */
  async function flushList(tickets: Ticket[] = [TICKET]) {
    const request = httpMock.expectOne((req) => req.url === API && req.method === 'GET');
    request.flush(tickets);
    await fixture.whenStable();
    return request;
  }

  it('loads tickets on init and renders them', async () => {
    await flushList();

    expect(fixture.nativeElement.textContent).toContain('Printer is jammed');
    expect(fixture.nativeElement.textContent).toContain('high');
  });

  it("preselects each ticket's current status in its dropdown", async () => {
    await flushList([{ ...TICKET, status: 'in_progress' }]);

    const select: HTMLSelectElement = fixture.nativeElement.querySelector('.ticket-table select');
    expect(select.value).toBe('in_progress');
  });

  it('shows an empty state when there are no tickets', async () => {
    await flushList([]);

    expect(fixture.nativeElement.textContent).toContain('No tickets yet');
  });

  it('shows an error message when the API is unreachable', async () => {
    const request = httpMock.expectOne((req) => req.url === API);
    request.flush(null, { status: 500, statusText: 'Server Error' });
    await fixture.whenStable();

    expect(fixture.nativeElement.textContent).toContain('Failed to load tickets');
  });

  it('reloads with a status filter when the dropdown changes', async () => {
    await flushList();

    const select: HTMLSelectElement = fixture.nativeElement.querySelector('.filter select');
    select.value = 'closed';
    select.dispatchEvent(new Event('change'));
    await fixture.whenStable();

    const request = httpMock.expectOne((req) => req.url === API && req.method === 'GET');
    expect(request.request.params.get('status')).toBe('closed');
    request.flush([]);
    await fixture.whenStable();
  });

  it('patches the status and refreshes the list', async () => {
    await flushList();

    const select: HTMLSelectElement = fixture.nativeElement.querySelector('.ticket-table select');
    select.value = 'closed';
    select.dispatchEvent(new Event('change'));
    await fixture.whenStable();

    const patch = httpMock.expectOne(`${API}/1`);
    expect(patch.request.method).toBe('PATCH');
    expect(patch.request.body).toEqual({ status: 'closed' });
    patch.flush({ ...TICKET, status: 'closed' });
    await fixture.whenStable();

    await flushList([{ ...TICKET, status: 'closed' }]);
  });

  it('deletes a ticket and refreshes the list', async () => {
    await flushList();

    const button: HTMLButtonElement = fixture.nativeElement.querySelector('.button--danger');
    button.click();
    await fixture.whenStable();

    const remove = httpMock.expectOne(`${API}/1`);
    expect(remove.request.method).toBe('DELETE');
    remove.flush(null, { status: 204, statusText: 'No Content' });
    await fixture.whenStable();

    await flushList([]);
    expect(fixture.nativeElement.textContent).not.toContain('Printer is jammed');
  });
});
