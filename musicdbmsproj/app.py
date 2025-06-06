from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_connection

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# ✅ Generic CRUD Route Generator with Unique Endpoints
def generic_crud_routes(entity, fields, id_field):
    def insert_func():
        if request.method == 'POST':
            data = tuple(request.form.get(field) for field in fields)
            placeholders = ', '.join([":" + str(i + 1) for i in range(len(fields))])
            sql = f"INSERT INTO {entity.upper()} ({', '.join(fields)}) VALUES ({placeholders})"
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(sql, data)
                conn.commit()
                flash("Insert successful", "success")
            except Exception as e:
                flash(str(e), "danger")
            finally:
                cursor.close()
                conn.close()
            return redirect(url_for(f"insert_{entity}"))
        return render_template(f"{entity}/insert.html")

    def view_func():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {entity.upper()}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template(f"{entity}/view.html", **{entity: rows})

    def delete_func():
        if request.method == 'POST':
            pk = request.form.get(id_field)
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(f"DELETE FROM {entity.upper()} WHERE {id_field} = :1", (pk,))
                conn.commit()
                flash("Delete successful", "success")
            except Exception as e:
                flash(str(e), "danger")
            finally:
                cursor.close()
                conn.close()
            return redirect(url_for(f"delete_{entity}"))
        return render_template(f"{entity}/delete.html")

    def update_func():
        if request.method == 'POST':
            pk = request.form.get(id_field)
            updates = {field: request.form.get(field) for field in fields if request.form.get(field)}
            if updates:
                set_clause = ", ".join([f"{field} = :{i + 1}" for i, field in enumerate(updates)])
                values = list(updates.values()) + [pk]
                conn = get_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute(f"UPDATE {entity.upper()} SET {set_clause} WHERE {id_field} = :{len(values)}", values)
                    conn.commit()
                    flash("Update successful", "success")
                except Exception as e:
                    flash(str(e), "danger")
                finally:
                    cursor.close()
                    conn.close()
            return redirect(url_for(f"update_{entity}"))
        return render_template(f"{entity}/update.html")

    # ✅ Register routes
    app.add_url_rule(f"/{entity}/insert", view_func=insert_func, methods=["GET", "POST"], endpoint=f"insert_{entity}")
    app.add_url_rule(f"/{entity}/view", view_func=view_func, methods=["GET"], endpoint=f"view_{entity}")
    app.add_url_rule(f"/{entity}/delete", view_func=delete_func, methods=["GET", "POST"], endpoint=f"delete_{entity}")
    app.add_url_rule(f"/{entity}/update", view_func=update_func, methods=["GET", "POST"], endpoint=f"update_{entity}")

# 🔹 Home Page
@app.route('/')
def home():
    return render_template("home.html")

# ✅ Register CRUD Routes (Final corrected version)
generic_crud_routes("users", ["userid", "username", "emailid", "membership", "phoneno"], "userid")
generic_crud_routes("playlists", ["playlistid", "playlistname", "userid", "noofsongs", "totaltime"], "playlistid")
generic_crud_routes("songs", ["songid", "songname", "artistid", "albumid", "releasedyear"], "songid")
generic_crud_routes("albums", ["albumid", "albumname","artistid","totaltime","noofsongs", "releasedyear"], "albumid")
generic_crud_routes("artists", ["artistid", "artistname", "entertainmentid", "instaid", "debutyear", "noofsongsreleased"], "artistid")
generic_crud_routes("entertainment", ["entertainmentid", "entertainmentname", "startedyear", "phonenumber"], "entertainmentid")
generic_crud_routes("member", ["memberid", "membername", "typeofmembership", "emailid", "userid"], "memberid")

# 🔹 Run App
if __name__ == '__main__':
    app.run(debug=True)
