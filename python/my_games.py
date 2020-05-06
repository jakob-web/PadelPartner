from flask import Flask, render_template, request, redirect
from os import listdir
from db_operations import insert, fetchall
import psycopg2





def show_my_matches():
    
    games = fetchall("select ort, klass, antal, info, skapare from match where skapare = %s, session["username"]