from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app.models import Ticket, Comment
from app.forms import TicketCreateForm, TicketUpdateForm, CommentForm
from app import db
from datetime import datetime
from sqlalchemy import select
from app.tickets import bp

@bp.route('/tickets')
@login_required
def list_tickets():
    if current_user.is_admin:
        stmt = select(Ticket).order_by(Ticket.created_at.desc())
        tickets = db.session.execute(stmt).scalars().all()
    else:
        stmt = select(Ticket).where(Ticket.author == current_user).order_by(Ticket.created_at.desc())
        tickets = db.session.execute(stmt).scalars().all()
    return render_template('tickets/list.html', tickets=tickets)


# The route to create a new ticket
@bp.route('/tickets/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketCreateForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            status='open',
            author=current_user
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket has been created!', 'success')
        return redirect(url_for('tickets.list_tickets'))
    return render_template('tickets/create.html', form=form)

# Route to add a comment to a ticket
@bp.route('/tickets/<int:ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    stmt = select(Ticket).where(Ticket.id == ticket_id)
    ticket = db.session.execute(stmt).scalars().first()
    if ticket is None:
     
        from flask import abort
        abort(404)
        
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            author=current_user,
            ticket=ticket
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    
    return redirect(url_for('tickets.view_ticket', id=ticket_id))


# The route to view a psecific ticket
@bp.route('/tickets/<int:id>')
@login_required
def view_ticket(id):
    stmt = select(Ticket).where(Ticket.id == id)
    ticket = db.session.execute(stmt).scalars().first()
    if ticket is None:
        from flask import abort
        abort(404)
        
    form = CommentForm()
    return render_template('tickets/view.html', ticket=ticket, form=form)

# The route to update an existing ticket
@bp.route('/tickets/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_ticket(id):
    stmt = select(Ticket).where(Ticket.id == id)
    ticket = db.session.execute(stmt).scalars().first()
    if ticket is None:
        from flask import abort
        abort(404)

    if not current_user.is_admin and ticket.author != current_user:
        flash('You cannot modify this ticket.')
        return redirect(url_for('tickets.view_ticket', id=id))
    
    form = TicketUpdateForm()

    if not current_user.is_admin:
        del form.status  

    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.priority = form.priority.data


        if current_user.is_admin and hasattr(form, 'status'):
            ticket.status = form.status.data

        ticket.updated_at = datetime.now()
        db.session.commit()
        flash('Ticket has been updated successfully.', 'success')
        return redirect(url_for('tickets.view_ticket', id=id))

    elif request.method == 'GET':
        form.title.data = ticket.title
        form.description.data = ticket.description
        form.priority.data = ticket.priority
        if current_user.is_admin and hasattr(form, 'status'):
            form.status.data = ticket.status

    return render_template('tickets/update.html', form=form, ticket=ticket)

# The final route to delete a ticket
@bp.route('/tickets/<int:id>/delete', methods=['GET'])
@login_required
def delete_ticket(id):
    if not current_user.is_admin:
        flash('Only administrators can delete tickets.')
        return redirect(url_for('tickets.list_tickets'))
    
    stmt = select(Ticket).where(Ticket.id == id)
    ticket = db.session.execute(stmt).scalars().first()
    if ticket is None:
        from flask import abort
        abort(404)

    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket has been deleted successfully.', 'success')
    return redirect(url_for('tickets.list_tickets'))
