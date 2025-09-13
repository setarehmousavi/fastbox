from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ParcelForm, ParcelStatusForm
from .models import Parcel, TrackingEvent

def home(request):
    return redirect('shipment:track_search')


@login_required
def parcel_create(request):
    tracking_info = None  # Will store tracking data to show in template

    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.sender = request.user
            parcel.save()

            # Prepare tracking info to show in template
            tracking_info = {
                'tracking_code': parcel.tracking_code,
                'estimated_price': parcel.estimated_price,
                'estimated_days': parcel.estimated_days
            }
    else:
        form = ParcelForm()

    return render(request, 'parcel/parcel_create.html', {
        'form': form,
        'tracking_info': tracking_info
    })



def track_search(request):
    if request.method == 'POST':
        code = request.POST.get('tracking_code', '').strip()
        if code:
            return redirect('shipment:track_result', tracking_code=code)
    return render(request, 'parcel/track_search.html')


def track_result(request, tracking_code):
    parcel = get_object_or_404(Parcel, tracking_code=tracking_code)
    events = parcel.events.all()
    return render(request, 'parcel/track_result.html', {'parcel': parcel, 'events': events})


@login_required
def dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "شما اجازه دسترسی به این صفحه را ندارید.")
        return redirect('user:index')

    # Exclude cancelled parcels from dashboard
    parcels = Parcel.objects.exclude(status='cancelled').order_by('-created_at')

    # Attach status form to each parcel for inline editing
    for parcel in parcels:
        parcel.status_form = ParcelStatusForm(instance=parcel)

    if request.method == 'POST':
        parcel_id = request.POST.get('parcel_id')
        parcel = get_object_or_404(Parcel, id=parcel_id)

        form = ParcelStatusForm(request.POST, instance=parcel)
        if form.is_valid():
            updated_parcel = form.save()

            # Create a TrackingEvent automatically
            TrackingEvent.objects.create(
                parcel=updated_parcel,
                status=updated_parcel.status,
                location="",
                note="وضعیت توسط ادمین تغییر کرد"
            )

            messages.success(request, f'وضعیت مرسوله {updated_parcel.tracking_code} تغییر کرد.')
            return redirect('shipment:dashboard')
        else:
            messages.error(request, "فرم تغییر وضعیت معتبر نیست.")

    return render(request, 'parcel/dashboard.html', {'parcels': parcels})

