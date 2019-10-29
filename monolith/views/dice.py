# Debug
import json
from flask import Blueprint, redirect, render_template, request, jsonify
from monolith.database import db, Story, Like, Dice, retrieve_dice_set, store_dice_set
from monolith.classes import Die, DiceSet

dice = Blueprint('dice', __name__)

@dice.route('/dice')
def show_dice_sets():
    dice_set = retrieve_dice_set()
    return jsonify(dice_set.serialize())
