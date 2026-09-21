<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class UserSetting extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'objetivo',
        'modo_anonimo',
        'alerta_sintomas',
    ];

    protected $casts = [
        'modo_anonimo' => 'boolean',
        'alerta_sintomas' => 'boolean',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
