<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Order;
use PDF;

class ReportController extends Controller
{
    public function salesReport(Request $request)
    {
        $type = $request->query('type', 'weekly');
        $orders = Order::query();

        if ($type === 'weekly') {
            $orders->where('created_at', '>=', now()->subWeek());
        } elseif ($type === 'monthly') {
            $orders->where('created_at', '>=', now()->subMonth());
        } elseif ($type === 'yearly') {
            $orders->where('created_at', '>=', now()->subYear());
        }

        $data = [
            'orders' => $orders->get(),
            'type' => $type,
        ];

        if ($request->query('download') === 'pdf') {
            $pdf = PDF::loadView('reports.sales', $data);
            return $pdf->download('sales_report.pdf');
        }

        return view('reports.sales', $data);
    }
}