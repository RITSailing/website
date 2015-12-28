var keystone = require('keystone');
var Types = keystone.Field.Types;

/**
 * Post Model
 * ==========
 */

var Request = new keystone.List('Member Request', {
	map: { name: 'email' },
	autokey: { path: 'slug', from: 'email', unique: true }
});

Request.add({
	name: { type: Types.Name, required: true, initial: true, index: true },
	email: { type: Types.Email, initial: true, required: true, index: true },
	year_level: { type: Types.Select, initial: true, options: '1st, 2nd, 3rd, 4th, 5th', required: true },
});

Request.defaultColumns = 'name, email, year_level';
Request.register();
